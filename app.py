from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API de Tarefas")

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

tarefas: List[Tarefa] = []

@app.post("/adicionar", status_code=201)
def adicionar_tarefa(tarefa: Tarefa):
    if any(t.nome == tarefa.nome for t in tarefas):
        raise HTTPException(status_code=400, detail="Já existe uma tarefa com esse nome.")
    tarefas.append(tarefa)
    return {"message": "Tarefa adicionada com sucesso!", "tarefa": tarefa}

@app.get("/listar", response_model=List[Tarefa])
def listar_tarefas():
    return tarefas

@app.put("/tarefa/{nome}/concluir", response_model=Tarefa)
def concluir_tarefa(nome: str):
    for i, t in enumerate(tarefas):
        if t.nome == nome:
            tarefas[i] = t.model_copy(update={"concluida": True})
            return tarefas[i]
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete("/remover/{nome}")
def remover_tarefa(nome: str):
    for i, t in enumerate(tarefas):
        if t.nome == nome:
            tarefas.pop(i)
            return {"message": "Tarefa removida com sucesso!"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
