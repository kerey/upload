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
        # this uploads file
        file_serializer = FileSerializer(data=request.data)
        # this is file validation
        if file_serializer.is_valid():
            # save file in directory static/images
            file_serializer.save()
            # test function generates gui file and saves it in directory static/code
            # then returns path for that gui file
            gui_file_path = test(file_serializer.data['file'])
            # compile function gets gui file path, converts it to html and returns entire html
            html = compile(gui_file_path)
            print(html)
            # finally, return html as response
            zip_file = open(html, 'rb')
            response = HttpResponse(FileWrapper(zip_file), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'CDX_COMPOSITES_20140626.zip'
            return response
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
