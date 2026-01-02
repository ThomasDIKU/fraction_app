from flask import Flask, render_template, request, send_file, jsonify
import tempfile

# NY importsti efter omstrukturering
from pdf.generator import build_pdf

app = Flask(__name__)


# -------------------------------------------------
# Vis forsiden (KUN GET)
# -------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# -------------------------------------------------
# Generér PDF ud fra frontend-brøker
# -------------------------------------------------
@app.route("/generate-pdf", methods=["POST"])
def generate_pdf_route():
    data = request.get_json()

    if not data or "fractions" not in data:
        return jsonify({"error": "Ingen brøker modtaget"}), 400

    representations = data.get("representations")
    if not representations:
        representations = None


    parsed = []

    try:
        for f in data["fractions"]:
            n = int(f["n"])
            d = int(f["d"])

            if n <= 0 or d <= 0 or n >= d:
                return jsonify({"error": "Ugyldig brøk"}), 400

            parsed.append((n, d))
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Forkert dataformat"}), 400

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()

    build_pdf(
        tmp.name,
        parsed,
        representations=representations
    )

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name="broekkort.pdf"
    )


# -------------------------------------------------
# Start server
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
