from flask import Flask, render_template, request
import os
import re
from apkutils import APK

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


HIGH_RISK = {
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
}


MEDIUM_RISK = {
    "android.permission.READ_PHONE_STATE",
    "android.permission.CALL_PHONE",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.ACCESS_BACKGROUND_LOCATION",
    "android.permission.BLUETOOTH",
}


def calculate_risk(permissions):
    score = 0
    high_permissions = []
    medium_permissions = []

    for permission in permissions:

        if permission in HIGH_RISK:
            score += 15
            high_permissions.append(permission)

        elif permission in MEDIUM_RISK:
            score += 7
            medium_permissions.append(permission)

    score = min(score, 100)

    if score >= 60:
        level = "HIGH RISK"
    elif score >= 30:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return score, level, high_permissions, medium_permissions


def extract_permissions(apk_path):

    permissions = []

    try:
        with APK.from_file(apk_path) as apk:

            manifest = apk.get_manifest()

            found = re.findall(
                r'<uses-permission[^>]+android:name="([^"]+)"',
                manifest
            )

            permissions = sorted(set(found))

    except Exception as error:
        print("APK analysis error:", error)

    return permissions


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "apk_file" not in request.files:
        return render_template(
            "index.html",
            error="Please select an APK file."
        )

    file = request.files["apk_file"]

    if file.filename == "":
        return render_template(
            "index.html",
            error="Please select an APK file."
        )

    if not file.filename.lower().endswith(".apk"):
        return render_template(
            "index.html",
            error="Only APK files are supported."
        )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    permissions = extract_permissions(filepath)

    if not permissions:
        return render_template(
            "index.html",
            error="No permissions could be extracted from this APK."
        )

    score, level, high_permissions, medium_permissions = calculate_risk(
        permissions
    )

    return render_template(
        "index.html",
        filename=file.filename,
        permissions=permissions,
        score=score,
        level=level,
        high_permissions=high_permissions,
        medium_permissions=medium_permissions
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
