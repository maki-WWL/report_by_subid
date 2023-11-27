import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from datetime import datetime

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

            date_of_file = from_date_month.strftime("%m-%Y")
            first_date_str = first_date.strftime("%Y-%m-%d")
            second_date_str = second_date.strftime("%Y-%m-%d")

            # request.session["first_date"] = str(first_date)
            # request.session["second_date"] = str(second_date)

            # formatted_date = date_of_file.lstrip("0")
            formatted_date = get_month_range(from_date_month, to_date_month)
            print(formatted_date)

            create_excel(formatted_date, first_date_str, second_date_str)
            # resize_table()

            file_path = 'result.xlsx'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                # Повернути помилку, якщо файл не знайдено
                return HttpResponse("Error: File not found", status=404)
