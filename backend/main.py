from fastapi import FastAPI, UploadFile, Form
import csv
import io
import statistics

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Welcome to Sales Anomalies Detector API! Use /upload-csv/ to upload your data."}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile, user_email: str = Form(...)):
    content = await file.read()
    decoded = content.decode("utf-8")
    lines = list(csv.reader(io.StringIO(decoded)))

    # Find the first row that looks like a header
    header_row_index = None
    for i, row in enumerate(lines):
        if "sales" in [cell.lower().strip() for cell in row]:
            header_row_index = i
            break

    if header_row_index is None:
        return {"error": "No header row with 'sales' column found."}

    header = lines[header_row_index]
    data_rows = lines[header_row_index + 1:]

    anomalies = []
    valid_sales = []
    valid_rows = []

    last_valid_sale = None

    for i, row in enumerate(data_rows, start=header_row_index + 2):  # real CSV row number
        row_dict = dict(zip(header, row))
        sale_raw = row_dict.get("sales", "").strip()

        if not sale_raw:
            anomalies.append(f"⚠️ Missing value in column 'sales' on row {i}")
            continue

        try:
            sale = float(sale_raw)
        except ValueError:
            anomalies.append(f"⚠️ Invalid sales data on row {i}")
            continue

        if last_valid_sale is not None:
            change = (sale - last_valid_sale) / last_valid_sale if last_valid_sale else 0
            if change >= 0.3:
                anomalies.append(f"📈 Sales spiked by {int(change * 100)}% on row {i}")
            elif change <= -0.3:
                anomalies.append(f"📉 Sales dropped by {int(abs(change) * 100)}% on row {i}")

        last_valid_sale = sale
        valid_sales.append(sale)
        valid_rows.append((i, sale))

    if len(valid_sales) >= 2:
        mean = statistics.mean(valid_sales)
        std_dev = statistics.stdev(valid_sales)
        for i, sale in valid_rows:
            if abs(sale - mean) > 2 * std_dev:
                anomalies.append(f"🚨 Sales anomaly on row {i}: {sale} (outside 2 std dev)")

    return {
        "message": "CSV received",
        "rows": len(lines),
        "report": "\n".join(anomalies) if anomalies else "✅ No significant anomalies detected.",
        "user_email": user_email,
    }
