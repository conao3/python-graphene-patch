import flask
import flask_graphql
import graphene
import graphene_sqlalchemy
import graphene_sqlalchemy.converter
import sqlalchemy.engine
import sqlalchemy.ext.declarative
import sqlalchemy.ext.hybrid
import sqlalchemy.orm
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import String

# SQLAlchemy config

engine = sqlalchemy.engine.create_engine('sqlite:///db.sqlite3')
db_session = sqlalchemy.orm.scoped_session(
    sqlalchemy.orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    ),
)
Base = sqlalchemy.ext.declarative.declarative_base()
Base.query = db_session.query_property()


class DepartmentModel(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    @sqlalchemy.ext.hybrid.hybrid_property
    def name_len(self) -> int:
        return len(self.name)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

engineering = DepartmentModel(name='Engineering')
hr = DepartmentModel(name='Human Resources')
db_session.add(engineering)
db_session.add(hr)

db_session.commit()


# Graphene config


def convert_sqlalchemy_hybrid_method(hybrid_prop, resolver, **field_kwargs):
    if 'type' not in field_kwargs:
        field_kwargs['type'] = graphene.Int

    return graphene.Field(resolver=resolver, **field_kwargs)


graphene_sqlalchemy.converter.convert_sqlalchemy_hybrid_method = convert_sqlalchemy_hybrid_method


class Department(graphene_sqlalchemy.SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_departments = graphene_sqlalchemy.SQLAlchemyConnectionField(
        Department.connection,
    )


schema = graphene.Schema(query=Query)


# Flask config

app = flask.Flask(__name__)
app.debug = True


app.add_url_rule(
    '/graphql', view_func=flask_graphql.GraphQLView.as_view('graphql', schema=schema, graphiql=True),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
