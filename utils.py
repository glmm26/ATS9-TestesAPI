def validar_lista_tarefas(response):
    """Valida se a resposta contem uma lista de tarefas com a chave `completed`."""
    data = response.json()

    assert isinstance(data, list), (
        f"Esperava uma lista, mas recebeu: {type(data).__name__}"
    )
    assert data, "A lista de tarefas esta vazia."
    assert any("completed" in tarefa for tarefa in data), (
        "Nenhuma tarefa na lista contem a chave 'completed'."
    )
