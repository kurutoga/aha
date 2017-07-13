from app import db


class Module(db.Model):
    id = db.Column(db.Integer(), db.Sequence('module_id_seq'), primary_key=True)
    name = db.Column(db.String(255))
    serial = db.Column(db.Integer(), unique=True)
    parent = db.Column(db.Integer(), db.ForeignKey('module.id'))
    type = db.Column(db.String(50))
    data = db.Column(db.JSON)


#event.listen(
#        Module.__table__,
#        "after_create",
#        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10001;")
#)
