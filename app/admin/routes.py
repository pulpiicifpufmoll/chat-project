# from flask import Flask, render_template, request, jsonify, session, redirect
# from langchain_community.document_loaders import TextLoader, PyPDFDirectoryLoader
# from langchain_text_splitters import CharacterTextSplitter
# from flask_login import login_required
# from . import bp_admin
# from app.auth.utils import admin_required

# @bp_admin.route('/admin', methods=['GET'])
# @login_required
# @admin_required
# def admin():
#     return render_template("admin/admin.html")


# @bp_admin.route('/ingest/file', methods=['GET', 'POST', 'DELETE'])
# @login_required
# @admin_required
# def files():
#     pass

# @bp_admin.route('/health', methods=['GET'])
# @login_required
# @admin_required
# def keepAlive():
#     pass

# # -------- H I L O S --------------

# # import threading
# # from flask import current_app

# # def process_pdf(pdf_file):
# #     # Simula el procesamiento del archivo PDF (puede ser una tarea intensiva)
# #     print("Procesando archivo PDF:", pdf_file)
# #     # Simula el tiempo de procesamiento
# #     import time
# #     time.sleep(5)
# #     print("Procesamiento completado para:", pdf_file)

# # @app.route('/admin/upload_pdf', methods=['POST'])
# # def upload_pdf():
# #     # Lógica para cargar el archivo PDF aquí
# #     pdf_file = request.files['pdf']
# #     if pdf_file:
# #         # Inicia un hilo para procesar el archivo PDF
# #         thread = threading.Thread(target=process_pdf, args=(pdf_file.filename,))
# #         thread.start()
# #         # Muestra un mensaje al usuario mientras se procesa el PDF en segundo plano
# #         flash("El archivo PDF se está procesando en segundo plano. Se notificará cuando se complete.")
# #         return redirect(url_for('admin_dashboard'))
# #     else:
# #         flash("No se ha seleccionado ningún archivo PDF.")
# #         return redirect(url_for('admin_dashboard'))
