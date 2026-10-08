# 📐 DAX Measures Catalog: Event Photo SaaS Feasibility & Investment Analysis
**Project:** Feasibility Study & Predictive Investment Analysis (QR Event Photo SaaS)  
**Tools:** Power BI Desktop / Service  

---

## 1. Unit Economics & Margin Measures

### [Gross Revenue per Event]
```DAX
Gross Revenue per Event = 
SELECTEDVALUE('dim_pricing_tiers'[package_price_idr], 250000)
```

### [Cloud Storage Cost per Event]
```DAX
Cloud Storage Cost per Event = 
VAR AvgPhotos = SELECTEDVALUE('dim_event_tiers'[avg_photos], 800)
VAR AvgPhotoSizeMB = 4.5
VAR TotalStorageGB = DIVIDE(AvgPhotos * AvgPhotoSizeMB, 1024, 0)
VAR S3PricePerGBMonthIDR = 365 -- ~USD 0.023/GB/month
VAR StorageMonths = [Selected Storage Retention Months]
RETURN
    TotalStorageGB * S3PricePerGBMonthIDR * StorageMonths
```

### [Payment Gateway Fee per Event]
```DAX
Payment Gateway Fee per Event = 
VAR FixedFee = 4000 -- Biaya transaksi virtual account / QRIS
VAR VariableRate = 0.015 -- 1.5% fee
RETURN
    FixedFee + ([Gross Revenue per Event] * VariableRate)
```

### [Net Contribution Margin per Event]
```DAX
Contribution Margin per Event = 
[Gross Revenue per Event] - (
    [Cloud Storage Cost per Event] + 
    [Payment Gateway Fee per Event] + 
    [Selected Estimated CAC]
)
```

### [Contribution Margin %]
```DAX
Contribution Margin % = 
DIVIDE([Contribution Margin per Event], [Gross Revenue per Event], 0)
```

---

## 2. Break-Even Point (BEP) & Payback Measures

### [Monthly Fixed OpEx]
```DAX
Monthly Fixed OpEx = 
SUM('fact_operating_expenses'[monthly_cost_idr]) -- Server dasar, domain, tools, maintenance
```

### [Break-Even Event Volume per Month]
```DAX
BEP Events per Month = 
DIVIDE(
    [Monthly Fixed OpEx],
    [Contribution Margin per Event],
    0
)
```

### [Initial Capital Expenditure (CapEx)]
```DAX
Total CapEx = 
SUM('fact_capital_expenses'[capex_cost_idr]) -- Biaya pengembangan web app awal
```

### [Payback Period (Months)]
```DAX
Payback Period Months = 
VAR MonthlyNetCashflow = ([Contribution Margin per Event] * [Selected Monthly Event Target]) - [Monthly Fixed OpEx]
RETURN
    IF(
        MonthlyNetCashflow <= 0,
        999, -- Tidak akan pernah balik modal jika cashflow negatif
        DIVIDE([Total CapEx], MonthlyNetCashflow, 0)
    )
```

---

## 3. Monte Carlo Predictive Risk Measures

### [Median Simulated NPV 24 Months]
```DAX
Median Simulated NPV = 
MEDIAN('fact_monte_carlo_runs'[npv_24m_idr])
```

### [Value at Risk (5th Percentile Bearish Scenario)]
```DAX
VaR 5th Percentile = 
PERCENTILE.INC('fact_monte_carlo_runs'[npv_24m_idr], 0.05)
```

### [Probability of Profitability %]
```DAX
Probability of Profit % = 
VAR ProfitableRuns = CALCULATE(COUNTROWS('fact_monte_carlo_runs'), 'fact_monte_carlo_runs'[is_profitable_24m] = 1)
VAR TotalRuns = COUNTROWS('fact_monte_carlo_runs')
RETURN
    DIVIDE(ProfitableRuns, TotalRuns, 0)
```

---

## 4. What-If Parameter Integration Measures

### [Go / No-Go Decision Signal]
```DAX
Go No-Go Status = 
SWITCH(
    TRUE(),
    [Payback Period Months] <= 12 && [Probability of Profit %] >= 0.75, "✅ GO (Sangat Layak)",
    [Payback Period Months] <= 18 && [Probability of Profit %] >= 0.60, "⚠️ CONDITIONAL (Layak dengan Syarat B2B)",
    "❌ NO-GO (Rekomendasi Tutup / Terlalu Berisiko)"
)
```
