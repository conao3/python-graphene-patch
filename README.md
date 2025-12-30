# python-graphene-patch

A workaround for graphene-sqlalchemy's hybrid property type inference issue.

## Overview

When using SQLAlchemy hybrid properties with graphene-sqlalchemy, the library doesn't properly infer field types from Python type annotations. This project demonstrates how to monkey-patch `convert_sqlalchemy_hybrid_method` to provide default type handling.

## The Problem

graphene-sqlalchemy fails to convert hybrid properties like:

```python
@sqlalchemy.ext.hybrid.hybrid_property
def name_len(self) -> int:
    return len(self.name)
```

The type annotation `-> int` is ignored, causing schema generation issues.

## The Solution

This project patches `graphene_sqlalchemy.types.convert_sqlalchemy_hybrid_method` to supply a default type when none is specified:

```python
def convert_sqlalchemy_hybrid_method(hybrid_prop, resolver, **field_kwargs):
    if 'type' not in field_kwargs:
        field_kwargs['type'] = graphene.Int

    return graphene.Field(resolver=resolver, **field_kwargs)

graphene_sqlalchemy.types.convert_sqlalchemy_hybrid_method = convert_sqlalchemy_hybrid_method
```

## Requirements

- Python 3.10+
- Poetry

## Getting Started

```bash
poetry env use 3.10
poetry install
```

## Running Tests

```bash
poetry run pytest -vv
```

## Running the Server

```bash
poetry run python main.py
```

Then open http://localhost:5000/graphql to access GraphiQL.

## License

Apache License 2.0
