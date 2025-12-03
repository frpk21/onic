import os
from datetime import datetime, date, time
import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from dashboard.models import ChiaDataset


def normalize_colname(col):
    value = str(col).strip().lower().replace(" ", "_").replace("-", "_").replace("__", "_")
    return value


def parse_date_time_parts(date_val, time_val):
    if pd.isna(date_val) and pd.isna(time_val):
        return None
    d_raw = None if pd.isna(date_val) else str(date_val).strip()
    t_raw = None if pd.isna(time_val) else str(time_val).strip()
    if d_raw:
        dt = pd.to_datetime(d_raw, dayfirst=False, errors='coerce')
        if pd.notna(dt):
            if t_raw and ":" in t_raw and dt.time() == time(0, 0):
                try:
                    parsed_time = datetime.strptime(t_raw, "%H:%M:%S").time() if t_raw.count(
                        ':') == 2 else datetime.strptime(t_raw, "%H:%M").time()
                    return datetime.combine(dt.date(), parsed_time)
                except Exception:
                    return dt.to_pydatetime()
            return dt.to_pydatetime()
    if d_raw:
        dt = pd.to_datetime(d_raw, dayfirst=True, errors='coerce')
        if pd.notna(dt):
            if t_raw and ":" in t_raw:
                try:
                    parsed_time = datetime.strptime(t_raw, "%H:%M:%S").time() if t_raw.count(
                        ':') == 2 else datetime.strptime(t_raw, "%H:%M").time()
                    return datetime.combine(dt.date(), parsed_time)
                except Exception:
                    return dt.to_pydatetime()
            return dt.to_pydatetime()
    if (not d_raw) and t_raw and ":" in t_raw:
        try:
            parsed_time = datetime.strptime(t_raw, "%H:%M:%S").time() if t_raw.count(':') == 2 else datetime.strptime(
                t_raw, "%H:%M").time()
            return datetime.combine(date(1970, 1, 1), parsed_time)
        except Exception:
            return None
    return None


class Command(BaseCommand):
    help = "Carga CSV en ChiaDataset combinando v_fecha + h_visita en v_fecha y coercion de tipos."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Ruta al archivo CSV")
        parser.add_argument("--batch", type=int, default=500, help="Batch size para bulk_create")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        batch_size = options["batch"]

        if not os.path.exists(csv_path):
            raise CommandError(f"Archivo no encontrado: {csv_path}")

        self.stdout.write(self.style.NOTICE(f"Leyendo CSV: {csv_path}"))
        try:
            df = pd.read_csv(csv_path, low_memory=False)
        except Exception as e:
            raise CommandError(f"Error leyendo CSV: {e}")

        self.stdout.write(self.style.SUCCESS(f"{len(df)} filas encontradas."))

        df.columns = [normalize_colname(c) for c in df.columns]

        date_col = "v_fecha" if "v_fecha" in df.columns else ("vfecha" if "vfecha" in df.columns else None)
        time_col = "h_visita" if "h_visita" in df.columns else ("hvisita" if "hvisita" in df.columns else None)

        if date_col or time_col:
            self.stdout.write(self.style.NOTICE("Combinando columnas v_fecha + h_visita en v_fecha..."))
            combined = []
            for idx, row in df.iterrows():
                d_val = row[date_col] if date_col and date_col in df.columns else None
                t_val = row[time_col] if time_col and time_col in df.columns else None
                dt = parse_date_time_parts(d_val, t_val)
                combined.append(dt)
            df["v_fecha"] = combined
            if time_col and time_col in df.columns:
                df = df.drop(columns=[time_col])

        model_fields = {f.name: f for f in ChiaDataset._meta.get_fields() if f.concrete}
        df_cols_in_model = [c for c in df.columns if c in model_fields]
        df = df[df_cols_in_model]

        objects = []
        errors = 0

        for i, row in df.iterrows():
            data = row.to_dict()

            for key, val in list(data.items()):
                if pd.isna(val):
                    data[key] = None
                    continue

                field = model_fields.get(key)
                if not field:
                    continue
                ftype = field.get_internal_type()

                # DateTime / Date / Time
                if ftype == "DateTimeField":
                    if isinstance(val, pd.Timestamp):
                        data[key] = val.to_pydatetime()
                    elif isinstance(val, datetime):
                        data[key] = val
                    else:
                        parsed = parse_date_time_parts(val, None)
                        data[key] = parsed
                elif ftype == "DateField":
                    try:
                        parsed = pd.to_datetime(val, dayfirst=False, errors='coerce')
                        data[key] = parsed.date() if pd.notna(parsed) else None
                    except Exception:
                        data[key] = None
                elif ftype == "TimeField":
                    try:
                        if isinstance(val, str) and ":" in val:
                            data[key] = datetime.strptime(val, "%H:%M:%S").time() if val.count(
                                ':') == 2 else datetime.strptime(val, "%H:%M").time()
                        else:
                            data[key] = None
                    except Exception:
                        data[key] = None

                elif ftype in ("BigIntegerField", "IntegerField"):
                    try:
                        data[key] = int(float(val))
                    except Exception:
                        data[key] = None
                elif ftype == "FloatField":
                    try:
                        data[key] = float(str(val).replace(',', '.'))
                    except Exception:
                        data[key] = None

                elif ftype == "CharField":
                    try:
                        s = str(val)
                        maxlen = getattr(field, "max_length", 255) or 255
                        if len(s) > maxlen:
                            s = s[:maxlen]
                        data[key] = s
                    except Exception:
                        data[key] = None
                else:
                    try:
                        data[key] = str(val)
                    except Exception:
                        data[key] = None

            try:
                objects.append(ChiaDataset(**data))
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.WARNING(f"Fila {i} ignorada por error creando instancia: {e}"))
                continue

        total = len(objects)
        self.stdout.write(self.style.NOTICE(f"Guardando {total} objetos en la BD (batch={batch_size})..."))

        ChiaDataset.objects.all().delete()
        try:
            with transaction.atomic():
                ChiaDataset.objects.bulk_create(objects, batch_size=batch_size)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"bulk_create falló: {e}. Intentando guardar por fila para debug..."))
            for idx, obj in enumerate(objects):
                try:
                    obj.save()
                except Exception as ex:
                    self.stdout.write(self.style.ERROR(f"Error guardando fila {idx}: {ex}. Valores: {obj.__dict__}"))
                    raise CommandError(f"Error guardando en DB (fila {idx}): {ex}")
            raise

        self.stdout.write(
            self.style.SUCCESS(f"Carga completada: {total} registros insertados. Filas con error: {errors}"))
