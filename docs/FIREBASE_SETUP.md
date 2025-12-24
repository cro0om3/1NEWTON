# Firebase Integration Guide
## دليل التكامل مع Firebase

### Overview
تم تفعيل Firebase Firestore و Storage لـ sync real-time لجميع البيانات (المنتجات، الفواتير، العملاء، العروض).

### Firebase Setup ✅
- **Project ID**: newton-smart-home
- **Database**: Firestore (Cloud)
- **Storage**: Firebase Storage
- **Credentials**: `data/firebase_credentials.json` (stored locally, NOT in git)

### Collections (المجموعات)
```
firestore/
├── products/           # المنتجات
│   ├── Device
│   ├── Description
│   ├── UnitPrice
│   ├── Warranty
│   ├── ImageBase64
│   ├── created_at
│   └── updated_at
├── invoices/          # الفواتير
│   ├── base_id
│   ├── date
│   ├── type
│   ├── number
│   ├── amount
│   ├── client_name
│   ├── phone
│   ├── location
│   ├── created_at
│   └── updated_at
├── customers/         # العملاء
│   ├── client_name
│   ├── phone
│   ├── location
│   ├── email
│   ├── status
│   ├── notes
│   ├── created_at
│   └── updated_at
└── quotations/        # عروض الأسعار
    ├── base_id
    ├── date
    ├── number
    ├── amount
    ├── client_name
    ├── created_at
    └── updated_at
```

### Storage (التخزين)
```
gs://newton-smart-home.appspot.com/products/{product_id}/image.png
```

### Auto-Save Features (الحفظ التلقائي)
✅ **Products**: يتم حفظ كل منتج جديد في Firestore + Storage
✅ **Invoices**: يتم حفظ كل فاتورة في Firestore تلقائياً
✅ **Customers**: يتم حفظ كل عميل في Firestore
✅ **Quotations**: يتم حفظ كل عرض سعر في Firestore

### Code Location (مواقع الكود)
- **Firebase Utils**: `utils/firebase_utils.py`
- **Products Integration**: `pages_custom/products_page.py` (line ~90)
- **Invoices Integration**: `pages_custom/invoice_page.py` (line ~132)
- **Customers Integration**: `pages_custom/customers_page.py` (line ~177)
- **Quotations Integration**: `pages_custom/quotation_page.py` (line ~932)

### How It Works (كيفية العمل)
1. **عند إضافة منتج**: يتم استدعاء `save_product_to_firebase()` تلقائياً
2. **عند إضافة فاتورة**: يتم استدعاء `save_invoice_to_firebase()` تلقائياً
3. **عند إضافة عميل**: يتم استدعاء `save_customer_to_firebase()` تلقائياً
4. **عند إضافة عرض سعر**: يتم استدعاء `save_quotation_to_firebase()` تلقائياً

### Error Handling (معالجة الأخطاء)
- إذا فشل Firebase، سيتم الحفظ في Excel على أي حال
- لا يتم إيقاف التطبيق بسبب فشل Firebase
- جميع الأخطاء تُطبع في console للتتبع

### Image Handling (معالجة الصور)
- الصور تُحفظ في Firebase Storage كـ `.png`
- يتم تحويلها تلقائياً من Base64
- المسار: `products/{product_id}/image.png`

### Firestore Rules (قواعد الأمان)
للتطوير (Development):
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

للإنتاج (Production) - يُرجى تحديث:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /products/{document=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    match /invoices/{document=**} {
      allow read, write: if request.auth != null;
    }
    match /customers/{document=**} {
      allow read, write: if request.auth != null;
    }
    match /quotations/{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Storage Rules
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /products/{productId}/image.png {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### First Time Setup (الإعداد الأول)
إذا كنت تريد مزامنة البيانات الموجودة من Excel إلى Firebase:
```python
from utils.firebase_utils import sync_excel_to_firebase
sync_excel_to_firebase()
```

### Monitoring (المراقبة)
- اذهب إلى [Firebase Console](https://console.firebase.google.com/u/0/project/newton-smart-home/firestore/databases/-default-/data)
- شاهد البيانات في الوقت الفعلي في Firestore
- شاهد الصور في Storage
- تحقق من الأخطاء في Logs

### Notes (ملاحظات)
⚠️ **لا تُرسل firebase_credentials.json إلى GitHub**
✅ تم إضافتها في .gitignore تلقائياً

### Support
للمساعدة أو المشاكل:
1. تحقق من Firebase Console للأخطاء
2. اطّلع على console output للتحذيرات
3. تأكد من internet connection
4. تحقق من Firebase rules والصلاحيات
