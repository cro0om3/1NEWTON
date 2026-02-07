# ماذا تضع في Streamlit → App settings → Secrets

انسخ المحتوى أدناه **بالكامل** في مربع Secrets (بدل المحتوى الحالي أو أضف السطر الأول إذا كان عندك Firebase فقط).

---

## 1) سلسلة اتصال Supabase (قاعدة البيانات)

أضف هذا السطر في **أعلى** الملف:

```toml
DB_CONNECTION_STRING = "postgresql://postgres:wAv1f0hIdqdyO0mi@db.nlwodsutdczdwujiafni.supabase.co:5432/postgres"
```

---

## 2) Firebase (الموجود عندك في الصورة)

إما أن تبقيه كما هو في الصورة (نفس المفاتيح في الأعلى)، أو تضعه تحت قسم `[firebase]` كالتالي حتى يعمل التطبيق من الـ Secrets بدون ملف:

```toml
[firebase]
type = "service_account"
project_id = "newton-smart-home"
private_key_id = "f6f683ce72fde0d5a53d253fcf538dab8b029fdb"
private_key = """-----BEGIN PRIVATE KEY-----
(الصق هنا المفتاح الكامل من Firebase كما في صورتك أو من firebase_credentials.json)
-----END PRIVATE KEY-----"""
client_email = "الحساب من Firebase Console أو من الملف JSON"
client_id = "رقم من الملف JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "رابط من الملف JSON"
```

القيم `client_email`, `client_id`, `client_x509_cert_url` تأخذها من ملف `data/firebase_credentials.json` (من نفس المشروع في Firebase).

---

## 3) الشكل النهائي الكامل (للنسخ)

اجمع القسمين في مربع Secrets بهذا الشكل (واستبدل قيم Firebase الحقيقية من ملفك):

```toml
# قاعدة البيانات (Supabase)
DB_CONNECTION_STRING = "postgresql://postgres:wAv1f0hIdqdyO0mi@db.nlwodsutdczdwujiafni.supabase.co:5432/postgres"

# Firebase
[firebase]
type = "service_account"
project_id = "newton-smart-home"
private_key_id = "f6f683ce72fde0d5a53d253fcf538dab8b029fdb"
private_key = """-----BEGIN PRIVATE KEY-----
(المفتاح الكامل هنا)
-----END PRIVATE KEY-----"""
client_email = "firebase-adminsdk-xxxxx@newton-smart-home.iam.gserviceaccount.com"
client_id = "رقم من JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

- إذا كان عندك **فقط** Firebase في الصورة (بدون قسم `[firebase]`): التطبيق يدعم أيضاً أن تكون المفاتيح في الجذر؛ أضف السطر الأول `DB_CONNECTION_STRING = "..."` فوقها واترك بقية Firebase كما هي.
- بعد الحفظ انتظر دقيقة ثم أعد تشغيل التطبيق على Streamlit.
