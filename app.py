from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        industry = request.form.get('industry', 'Finance')
        records = int(request.form.get('records', 10000))
        data_sensitivity = request.form.get('sensitivity', 'Medium')
        
        # Base cost per record compromised varies by industry (based on IBM Cost of a Data Breach reports)
        industry_multipliers = {
            "Healthcare": 350,
            "Finance": 320,
            "Technology": 280,
            "E-Commerce": 210,
            "Education": 160
        }
        
        sensitivity_multipliers = {
            "Low": 0.8,
            "Medium": 1.2,
            "High": 1.8,
            "Critical (PII + Financial)": 2.5
        }
        
        base_cost_per_record = industry_multipliers.get(industry, 250)
        sens_multiplier = sensitivity_multipliers.get(data_sensitivity, 1.0)
        
        # Calculate Financial Loss
        financial_loss = records * base_cost_per_record * sens_multiplier
        
        # Calculate Legal & Compliance Costs (Regulatory fines like GDPR/HIPAA/CCPA)
        legal_costs = financial_loss * 0.35
        
        # Calculate Reputation Loss (Brand churn, lost customer trust)
        reputation_loss_value = financial_loss * 0.45
        
        # Total Potential Cost
        total_cost = financial_loss + legal_costs + reputation_loss_value
        
        # Reputation Score Rating
        if total_cost > 50_000_000:
            reputation_score = "Critical (Severe Brand Damage)"
            rep_width = "100%"
        elif total_cost > 10_000_000:
            reputation_score = "High (Significant Customer Churn)"
            rep_width = "75%"
        elif total_cost > 1_000_000:
            reputation_score = "Moderate (Noticeable Market Impact)"
            rep_width = "50%"
        else:
            reputation_score = "Low (Contained Impact)"
            rep_width = "25%"
            
        # Format currency nicely (in Millions/Thousands)
        def format_currency(amount):
            if amount >= 1_000_000:
                return f"${round(amount / 1_000_000, 2)}M"
            elif amount >= 1_000:
                return f"${round(amount / 1_000, 1)}K"
            else:
                return f"${round(amount, 2)}"

        result = {
            "industry": industry,
            "records": f"{records:,}",
            "sensitivity": data_sensitivity,
            "total_cost": format_currency(total_cost),
            "financial_loss": format_currency(financial_loss),
            "fin_width": f"{min(int((financial_loss / total_cost) * 100), 100)}%",
            "legal_costs": format_currency(legal_costs),
            "legal_width": f"{min(int((legal_costs / total_cost) * 100), 100)}%",
            "reputation_score": reputation_score,
            "rep_width": rep_width
        }

    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
