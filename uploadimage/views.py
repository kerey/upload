from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import FileSerializer
from pix2code.model.sample import test
from pix2code.compiler.web_compiler import compile
from wsgiref.util import FileWrapper
from django.http import HttpResponse

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            gui_file_path = test(file_serializer.data['file'])
            html = compile(gui_file_path)
            print(html)
            zip_file = open(html, 'rb')
            response = HttpResponse(FileWrapper(zip_file), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'CDX_COMPOSITES_20140626.zip'
            return response
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
