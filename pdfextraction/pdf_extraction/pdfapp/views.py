from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pdfapp.utils import extract_key_value_pairs, extract_tabular_data

def upload_file(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        file_path = fs.save(pdf_file.name, pdf_file)
        file_url = fs.url(file_path)
        file_extension = pdf_file.name.split('.')[-1].lower()
        if file_extension == 'pdf':
            extract_key_value_pairs(settings.MEDIA_ROOT + '/' + file_path)
            data = {'message': 'Data extracted successfully'}
        elif file_extension in ['jpg', 'jpeg']:
            extract_tabular_data(settings.MEDIA_ROOT + '/' + file_path)
            data = {'message': 'Data extracted successfully'}
        else:
            data = {'message': 'Unsupported file type'}
        return render(request, 'result.html', {'file_url': file_url, 'data': data})
    return render(request, 'upload.html')
