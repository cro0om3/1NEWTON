"""
Firebase Integration Utilities
التعامل مع Firebase Firestore و Storage للبيانات السحابية
"""

import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
import json
import os
import base64
from pathlib import Path
import streamlit as st

# تهيئة Firebase مرة واحدة فقط
_firebase_initialized = False

def init_firebase():
    """تهيئة Firebase مع Service Account Credentials (من ملف أو من st.secrets)"""
    global _firebase_initialized

    if _firebase_initialized:
        return True

    try:
        cred = None
        # 1) من Streamlit Secrets (مهم على Streamlit Cloud)
        _firebase_keys = (
            "type", "project_id", "private_key_id", "private_key",
            "client_email", "client_id", "auth_uri", "token_uri",
            "auth_provider_x509_cert_url", "client_x509_cert_url"
        )
        if hasattr(st, "secrets") and isinstance(st.secrets, dict):
            firebase_dict = st.secrets.get("firebase")
            if firebase_dict and isinstance(firebase_dict, dict):
                cred = credentials.Certificate(dict(firebase_dict))
            elif st.secrets.get("type") == "service_account":
                cred = credentials.Certificate({
                    k: v for k, v in st.secrets.items()
                    if k in _firebase_keys
                })

        # 2) من ملف محلي
        if cred is None:
            cred_path = Path(__file__).parent.parent / "data" / "firebase_credentials.json"
            if not cred_path.exists():
                return False
            cred = credentials.Certificate(str(cred_path))

        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return True
    except Exception as e:
        if hasattr(st, "error"):
            st.error(f"❌ خطأ في تهيئة Firebase: {str(e)}")
        return False

def get_firestore_client():
    """الحصول على Firestore client"""
    if not _firebase_initialized:
        if not init_firebase():
            return None
    return firestore.client()

def save_product_to_firebase(product_data):
    """
    حفظ منتج جديد إلى Firebase Firestore + Storage
    
    Args:
        product_data: dict بيانات المنتج (Device, Description, UnitPrice, Warranty, ImageBase64, etc.)
    
    Returns:
        bool: نجاح أو فشل العملية
    """
    try:
        db = get_firestore_client()
        if not db:
            return False
        
        # التحضير للبيانات
        product_to_save = product_data.copy()
        product_to_save['created_at'] = datetime.now().isoformat()
        product_to_save['updated_at'] = datetime.now().isoformat()
        
        # إزالة الصورة من البيانات الأساسية (سيتم حفظها في Storage)
        image_base64 = product_to_save.pop('ImageBase64', None)
        
        # حفظ في Firestore
        doc_ref = db.collection('products').document()
        product_to_save['product_id'] = doc_ref.id
        doc_ref.set(product_to_save)
        
        # حفظ الصورة في Storage إذا كانت موجودة
        if image_base64:
            try:
                save_product_image_to_storage(doc_ref.id, image_base64)
            except Exception as e:
                print(f"⚠️ تحذير: فشل حفظ الصورة: {str(e)}")
        
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حفظ المنتج: {str(e)}")
        return False

def save_product_image_to_storage(product_id, image_base64):
    """
    حفظ صورة المنتج في Firebase Storage
    
    Args:
        product_id: معرّف المنتج
        image_base64: الصورة في صيغة Base64
    """
    try:
        # تحويل Base64 إلى bytes
        if ',' in image_base64:
            image_data = base64.b64decode(image_base64.split(',')[1])
        else:
            image_data = base64.b64decode(image_base64)
        
        # حفظ في Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'products/{product_id}/image.png')
        blob.upload_from_string(image_data, content_type='image/png')
        
        return True
    except Exception as e:
        print(f"❌ خطأ في حفظ الصورة في Storage: {str(e)}")
        return False

def save_invoice_to_firebase(invoice_data):
    """
    حفظ فاتورة جديدة إلى Firebase Firestore
    
    Args:
        invoice_data: dict بيانات الفاتورة
    
    Returns:
        bool: نجاح أو فشل العملية
    """
    try:
        db = get_firestore_client()
        if not db:
            return False
        
        # التحضير للبيانات
        invoice_to_save = invoice_data.copy()
        invoice_to_save['created_at'] = datetime.now().isoformat()
        invoice_to_save['updated_at'] = datetime.now().isoformat()
        
        # حفظ في Firestore
        doc_ref = db.collection('invoices').document()
        invoice_to_save['invoice_id'] = doc_ref.id
        doc_ref.set(invoice_to_save)
        
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حفظ الفاتورة: {str(e)}")
        return False

def save_customer_to_firebase(customer_data):
    """
    حفظ عميل جديد إلى Firebase Firestore
    
    Args:
        customer_data: dict بيانات العميل (name, phone, location, email, etc.)
    
    Returns:
        bool: نجاح أو فشل العملية
    """
    try:
        db = get_firestore_client()
        if not db:
            return False
        
        # التحضير للبيانات
        customer_to_save = customer_data.copy()
        customer_to_save['created_at'] = datetime.now().isoformat()
        customer_to_save['updated_at'] = datetime.now().isoformat()
        
        # حفظ في Firestore
        doc_ref = db.collection('customers').document()
        customer_to_save['customer_id'] = doc_ref.id
        doc_ref.set(customer_to_save)
        
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حفظ العميل: {str(e)}")
        return False

def save_quotation_to_firebase(quotation_data):
    """
    حفظ عرض سعر جديد إلى Firebase Firestore
    
    Args:
        quotation_data: dict بيانات العرض
    
    Returns:
        bool: نجاح أو فشل العملية
    """
    try:
        db = get_firestore_client()
        if not db:
            return False
        
        # التحضير للبيانات
        quotation_to_save = quotation_data.copy()
        quotation_to_save['created_at'] = datetime.now().isoformat()
        quotation_to_save['updated_at'] = datetime.now().isoformat()
        
        # حفظ في Firestore
        doc_ref = db.collection('quotations').document()
        quotation_to_save['quotation_id'] = doc_ref.id
        doc_ref.set(quotation_to_save)
        
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حفظ العرض: {str(e)}")
        return False

def get_all_products_from_firebase():
    """
    جلب جميع المنتجات من Firebase
    
    Returns:
        list: قائمة المنتجات
    """
    try:
        db = get_firestore_client()
        if not db:
            return []
        
        docs = db.collection('products').stream()
        products = []
        for doc in docs:
            products.append(doc.to_dict())
        
        return products
    except Exception as e:
        print(f"❌ خطأ في جلب المنتجات: {str(e)}")
        return []

def get_all_customers_from_firebase():
    """
    جلب جميع العملاء من Firebase
    
    Returns:
        list: قائمة العملاء
    """
    try:
        db = get_firestore_client()
        if not db:
            return []
        
        docs = db.collection('customers').stream()
        customers = []
        for doc in docs:
            customers.append(doc.to_dict())
        
        return customers
    except Exception as e:
        print(f"❌ خطأ في جلب العملاء: {str(e)}")
        return []

def get_all_invoices_from_firebase():
    """
    جلب جميع الفواتير من Firebase
    
    Returns:
        list: قائمة الفواتير
    """
    try:
        db = get_firestore_client()
        if not db:
            return []
        
        docs = db.collection('invoices').stream()
        invoices = []
        for doc in docs:
            invoices.append(doc.to_dict())
        
        return invoices
    except Exception as e:
        print(f"❌ خطأ في جلب الفواتير: {str(e)}")
        return []

def delete_product_from_firebase(product_id):
    """حذف منتج من Firebase"""
    try:
        db = get_firestore_client()
        if not db:
            return False
        
        db.collection('products').document(product_id).delete()
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حذف المنتج: {str(e)}")
        return False

def delete_customer_from_firebase(customer_id):
    """حذف عميل من Firebase"""
    try:
        db = get_firestore_client()
        if not db:
            return False
        
        db.collection('customers').document(customer_id).delete()
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حذف العميل: {str(e)}")
        return False

def sync_excel_to_firebase():
    """
    مزامنة بيانات Excel الموجودة إلى Firebase (استخدم مرة واحدة فقط)
    """
    try:
        import pandas as pd
        
        # مزامنة المنتجات
        products_file = Path(__file__).parent.parent / "data" / "products.xlsx"
        if products_file.exists():
            df_products = pd.read_excel(products_file)
            for idx, row in df_products.iterrows():
                product_dict = row.to_dict()
                # تحويل NaN إلى None
                product_dict = {k: (None if pd.isna(v) else v) for k, v in product_dict.items()}
                save_product_to_firebase(product_dict)
        
        # مزامنة العملاء
        customers_file = Path(__file__).parent.parent / "data" / "customers.xlsx"
        if customers_file.exists():
            df_customers = pd.read_excel(customers_file)
            for idx, row in df_customers.iterrows():
                customer_dict = row.to_dict()
                customer_dict = {k: (None if pd.isna(v) else v) for k, v in customer_dict.items()}
                save_customer_to_firebase(customer_dict)
        
        return True
    except Exception as e:
        st.error(f"❌ خطأ في مزامنة البيانات: {str(e)}")
        return False
