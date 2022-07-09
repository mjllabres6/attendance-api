import os


def register():
    from app import app
    from app.classes.routes import module as class_module
    from app.students.routes import module as student_module
    from app.subjects.routes import module as subject_module
    from app.prof.routes import module as prof_module

    app.register_blueprint(class_module, url_prefix="/attendance-api")
    app.register_blueprint(student_module, url_prefix="/attendance-api")
    app.register_blueprint(subject_module, url_prefix="/attendance-api")
    app.register_blueprint(prof_module, url_prefix="/attendance-api")

    print(app.url_map)
