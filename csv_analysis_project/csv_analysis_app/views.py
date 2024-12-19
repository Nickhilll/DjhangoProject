from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
import os
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            # Perform basic analysis
            head = df.head().to_html()
            stats = df.describe().to_html()
            missing_summary = df.isnull().sum().reset_index(name='Missing Values').to_html(index=False)

            # Ensure media directory exists
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # Generate histogram for numerical columns
            numerical_cols = df.select_dtypes(include=['number']).columns
            if not numerical_cols.empty:
                plt.figure(figsize=(10, 6))
                df[numerical_cols].hist(bins=15)
                hist_path = os.path.join(settings.MEDIA_ROOT, 'histogram.png')
                plt.savefig(hist_path)
                plt.close()
                hist_url = settings.MEDIA_URL + 'histogram.png'
            else:
                hist_url = None

            return render(request, 'results.html', {
                'head': head,
                'stats': stats,
                'missing_summary': missing_summary,
                'hist_url': hist_url,
            })
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})
