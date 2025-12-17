##### THEM VAO HOME index.html #####

{% if user.is_authenticated %}
  Xin chào {{ user.username }}
{% else %}
  <a href="/login/">Login</a>
{% endif %}

##### THEM VAO CAC PAGE YEU CAU DANG NHAP #####

from django.contrib.auth.decorators import login_required
@login_required
# def fn()

