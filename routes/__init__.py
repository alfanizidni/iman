# routes/__init__.py
from .kampusMst_routes import kampusMst_routes
from .jurusan_routes import jurusan_routes
from .prodi_routes import prodi_routes
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from models.auth import Auth
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
