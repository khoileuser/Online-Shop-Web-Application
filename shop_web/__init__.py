
--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 660
Content-Type: application/octet-stream
X-File-MD5: c621a1be637776e10e8619c8764cff99
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/README.md

��#   O n l i n e - W e b - A p p l i c a t i o n  
  
 # #   I n s t a l l a t i o n  
 1 .   V i r t u a l   e n v i r o n m e n t  
 -   W i n d o w s  
 ` ` `  
 p y t h o n   - m   v e n v   v e n v   ;   v e n v \ S c r i p t s \ a c t i v a t e  
 ` ` `  
 -   L i n u x / M a c  
 ` ` `  
 p y t h o n   - m   v e n v   v e n v   ;   s o u r c e   v e n v / b i n / a c t i v a t e  
 ` ` `  
  
 2 .   I n s t a l l   r e q u i r e m e n t s  
 ` ` `  
 p i p   i n s t a l l   - r   r e q u i r e m e n t s . t x t  
 ` ` `  
  
 3 .   R u n   s e r v e r  
 ` ` `  
 p y t h o n   m a n a g e . p y   r u n s e r v e r  
 ` ` ` 
--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 409
Content-Type: application/octet-stream
X-File-MD5: 77ab5fca0753a07e88720591fc3e9a0a
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/shop_web/asgi.py

"""
ASGI config for shop_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_web.settings')

application = get_asgi_application()

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 835
Content-Type: application/octet-stream
X-File-MD5: 7ef97e145ea1f994c255168e06a4228e
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/shop_web/urls.py

"""
URL configuration for shop_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('web_app.urls')),
    path('admin/', admin.site.urls),
]

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 409
Content-Type: application/octet-stream
X-File-MD5: 07bd58a14843fd838f08416c9a49d405
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/shop_web/wsgi.py

"""
WSGI config for shop_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_web.settings')

application = get_wsgi_application()

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 0
Content-Type: application/octet-stream
X-File-MD5: d41d8cd98f00b204e9800998ecf8427e
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/web_app/__init__.py


--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 66
Content-Type: application/octet-stream
X-File-MD5: ef4c241c5311eee11a93e9366f492a72
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/web_app/admin.py

from django.contrib import admin

# Register your models here.

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 151
Content-Type: application/octet-stream
X-File-MD5: 67ff0cc556a0df89c991ab5863efbb68
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/web_app/apps.py

from django.apps import AppConfig


class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_app'

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 0
Content-Type: application/octet-stream
X-File-MD5: d41d8cd98f00b204e9800998ecf8427e
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/web_app/migrations/__init__.py


--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 63
Content-Type: application/octet-stream
X-File-MD5: e08f0582500f6562bf0a931ef9503b39
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/web_app/tests.py

from django.test import TestCase

# Create your tests here.

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 1510
Content-Type: application/octet-stream
X-File-MD5: d5ba96b869fdd30602e7afc9c155df36
X-File-Mtime: 1702357944
X-File-Path: /programs/education/Online-Shop-Web-Application/.git/objects/ee/eabff669b993d166a155ec8568edd987fcecd8

x�W�n�6�����ʕ��\Hn\�M�&��u����h�E*$��M��P�vu�mP�������(*CǇ��7>FB�K,���_ɣ�wg7\_��V�� q�� �H#&�������=�c�,A�$�0�Fn~�/"�7Kkk�>7|�F�S|���e�E�*i����)�X���bi��l]+m{�k��2�يS�ۗ���r"��D�t>;l�y7-������K�~gZ��F�u-8_�Lb/��A��L�#d75��+R����R��4��x�1��T49��I)c5���r�0�8ŭ	��y��y�4��;�3�Wz&��e]řR�U���l1;�snlL��m�*.g�����n3%c�[�r��ݤ�)���1�Y�gg�?k���n$��P���{I�;z�<�^��~�_���>5/~�����'z����o�~��4S��Q�\��Jn*�w�T��������߼�����B���{;@��|��	����A���'���ؗ<��d*� *�1pcK\CU�}���ȊmQ���3� �$Y���N,eD#������ev�e�[oP�Թ��dF��2羶�18q��`.sv�]�@A�ƙ��OՄB-�D��H����U�kN�Q'���j@y�k.�R���*D��k��VT	Ajú��9���5�����3f׌Io�	w�:��<�<X˦v���3O&}�]`�LT�`�4��B�a��*��E�ium[0�m�UU�+jb���Y�Tg�W�BjfVE�I�!"���t˳]���˟pKƋO��X��Ǜ�1vz��<��Mb2B�V��'.��p�eѴ| CY7v��Y�9um�A�>;���=� ��J@w��һ0"�,H��a�	I�X�d�gf%�_��lJ�n�]�U�NbG�[9��^�Z�2]���y�~��3K��=A�-6�O���q{�j�
�]�����p˿Qܧ��Cł}���4>���������Wf����dW�	܎����5�9���Qq{�A�>jx�Ÿ/��z��
&#�hs`0��tLn~��
��[k�����U����-o"�R���I�UR�;_������+ty�w�8�����s=P[�q�Qc�v3Yt�!<A=�� ����s�e���d�@G�[�#�����?�'���х2���V��7#��6�'��iC\�űV��:<}�[-��-��]����`�/=���l���s�a���԰'܉e_�Ƴ�d7�q�� 0"+��<W��i�(���܊@�����"ㆁ�10�y
t�۾�\�wq��7��ןk��C�ʫO��E��ʘ�эH��`D�I\��l[ɣKl�}�c��p�S_e�n�	�-�����z�|��fb����f����9���E;��
�Wg�=<�W����h�p���k�8��oG��=ݨ/`���/��}�C�0J��*����߷�7�
--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 85
Content-Type: application/octet-stream
X-File-MD5: b252e3ca04f126d5c8f11b4ccaf9e4e2
X-File-Mtime: 1702357944
X-File-Path: /programs/education/Online-Shop-Web-Application/.git/objects/e4/75d972733a9c94ccf293b2559bf1960a33f80e

x+)JMU0�`040031QH��/I-��(��a�$�����/�㌍_�W+�=��U����S���n9��z�<���i`�� L� a
--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 41
Content-Type: application/octet-stream
X-File-MD5: 0115b23fefb6533149ea0118e6a1e6ee
X-File-Mtime: 1702360004
X-File-Path: /programs/education/Online-Shop-Web-Application/.git/refs/heads/checkout

fab7cb238216277108b41e0d3a1b31c5a707a065

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 41
Content-Type: application/octet-stream
X-File-MD5: 366401d4070492d1870e0225919ebc7a
X-File-Mtime: 1702350008
X-File-Path: /programs/education/Online-Shop-Web-Application/.git/refs/heads/main

918be896c664da88e4c68caebca3fd7cf04861f5

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZtbEM7Im4suWK
Content-Length: 41
Content-Type: application/octet-stream
X-File-MD5: 77bc7292c278265712d1bceba1192069
X-File-Mtime: 1702358024
X-File-Path: /programs/education/Online-Shop-Web-Application/.git/refs/heads/product-seeding

9affd055c2474f2b0500b878ff17c9db24bf6611

--boundary_.oOo._NxvRF25l0LEmOI0pg+nZt