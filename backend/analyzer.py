import statistics

def find_anomalies(data):
    if not data or "sales" not in data[0]:
        return []

    anomalies = []
    sales_values = []

    # Collect all valid sales values for statistical analysis
    for row in data:
        try:
            sales = float(row["sales"])
            sales_values.append(sales)
        except:
            continue

    # Calculate mean and standard deviation
    if len(sales_values) < 2:
        return ["⚠️ Not enough valid sales data to analyze."]
    
    mean = statistics.mean(sales_values)
    stdev = statistics.stdev(sales_values)

    for i in range(len(data)):
        sales_str = data[i].get("sales", "")
        
        # Null or empty value check
        if not sales_str:
            anomalies.append(f"⚠️ Missing sales value on row {i+1}")
            continue
        
        try:
            curr = float(sales_str)
        except:
            anomalies.append(f"⚠️ Invalid number format for sales on row {i+1}")
            continue

        # Z-score-based anomaly
        if stdev > 0:
            z = abs((curr - mean) / stdev)
            if z > 2:
                anomalies.append(f"🚨 Sales value {curr} on row {i+1} is a statistical outlier (z-score = {z:.2f})")

        # % change anomaly
        if i > 0:
            try:
                prev = float(data[i-1]["sales"])
                if prev == 0:
                    continue
                change = (curr - prev) / prev
                if change >= 0.3:
                    anomalies.append(f"📈 Sales spiked by {int(change*100)}% on row {i+1}")
                elif change <= -0.3:
                    anomalies.append(f"📉 Sales dropped by {int(abs(change)*100)}% on row {i+1}")
            except:
                continue

    return anomalies
def generate_report(anomalies):
    if not anomalies:
        return "✅ No significant anomalies detected."
    return "\n".join(anomalies)
