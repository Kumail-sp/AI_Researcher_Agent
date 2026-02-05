from fpdf import FPDF

def create_pdf(input_file, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Read the agent's markdown output
    with open(input_file, "r") as f:
        content = f.read()

    # Add a Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Career Gap Analysis Report", ln=True, align='C')
    pdf.ln(10) # Add a line break

    # Add the Content
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content) # multi_cell handles line wrapping

    pdf.output(output_file)
    print(f"--- ✅ Professional PDF Generated: {output_file} ---")

if __name__ == "__main__":
    create_pdf("report.md", "Career_Analysis.pdf")