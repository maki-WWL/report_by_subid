import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from datetime import datetime
from zipfile import ZipFile

from kt_comparison.forms import DateForm
from kt_comparison.services.compare_files import create_excel, resize_table
from kt_comparison.utils import get_month_range


class IndexView(generic.View):
    template_name = 'report_by_subid/download_data.html'

    def get(self, request):
        form = DateForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = DateForm(request.POST)
        if form.is_valid():
            from_date_month = form.cleaned_data["from_date_month"]
            to_date_month = form.cleaned_data["to_date_month"]
            first_date = form.cleaned_data["first_date"]
            second_date = form.cleaned_data["second_date"]

            first_date_str = first_date.strftime("%Y-%m-%d")
            second_date_str = second_date.strftime("%Y-%m-%d")

            formatted_date = get_month_range(from_date_month, to_date_month)
            print(formatted_date)

            checkbox_tm = form.cleaned_data["checkbox_tm"]
            checkbox_tw = form.cleaned_data["checkbox_tw"]

            created_files = []
            if checkbox_tm:
                create_excel(formatted_date, first_date_str, second_date_str, folder_path='kt_1')
                created_files.append('result_kt_1.xlsx')
            if checkbox_tw:
                create_excel(formatted_date, first_date_str, second_date_str, folder_path='kt_2')
                created_files.append('result_kt_2.xlsx')
            # resize_table()

            if len(created_files) == 1:
                file_path = created_files[0]
                return self.generate_file_response(file_path)
            elif len(created_files) > 1:
                zip_file_path = self.create_zip_file(created_files)
                return self.generate_file_response(zip_file_path, content_type="application/zip", file_type="zip")
            else:
                return HttpResponse("Error: No files generated", status=404)
            
    def generate_file_response(self, file_path, content_type="application/vnd.ms-excel", file_type="xlsx"):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=content_type)
                response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
                return response
        else:
            return HttpResponse("Error: File not found", status=404)

    def create_zip_file(self, file_paths):
        zip_file_name = "results.zip"
        with ZipFile(zip_file_name, 'w') as zipf:
            for file in file_paths:
                zipf.write(file, os.path.basename(file))
        return zip_file_name