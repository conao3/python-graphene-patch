import graphene.test

import main


def test_main():
    client = graphene.test.Client(main.schema)
    result = client.execute('''
{
    allDepartments {
        edges {
            node {
                id
                name
            }
        }
    }
}
''')

    assert result == {
        'data': {
            'allDepartments': {
                'edges': [
                    {
                        'node': {
                            'id': 'RGVwYXJ0bWVudDox',
                            'name': 'Engineering',
                        },
                    },
                    {
                        'node': {
                            'id': 'RGVwYXJ0bWVudDoy',
                            'name': 'Human Resources',
                        },
                    },
                ],
            },
        },
    }


def test_hybrid_property():
    client = graphene.test.Client(main.schema)
    result = client.execute('''
{
    allDepartments {
        edges {
            node {
                name
                nameLen
            }
        }
    }
}
''')

    assert result == {
        'data': {
            'allDepartments': {
                'edges': [
                    {
                        'node': {
                            'name': 'Engineering',
                            'nameLen': 11,
                        },
                    },
                    {
                        'node': {
                            'name': 'Human Resources',
                            'nameLen': 15,
                        },
                    },
                ],
            },
        },
    }
