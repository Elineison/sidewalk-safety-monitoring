# Sidewalk Safety Monitoring

Estudo de caso público para monitoramento de permanência em calçadas por câmeras.

Este repositório é uma versão sanitizada de um fluxo de monitoramento de calçadas: ROI de câmera em contexto operacional Dahua/Intelbras, tracks de pessoas, limites de permanência, cooldowns, runtime, evidência sintética e eventos para operação. Ele foi feito para avaliação de portfólio sem expor câmeras, clientes ou incidentes reais.

## Problema Operacional

Monitoramento de calçadas é diferente de detecção genérica de movimento. O sistema precisa saber se uma pessoa permanece em uma ROI externa por tempo excessivo, se a câmera continua entregando frames recentes e se os alertas estão sendo criados com contexto suficiente para um operador agir.

## O Que Este Projeto Demonstra

- Módulo FastAPI para analytics de câmeras de calçada usando uma família operacional Dahua/Intelbras.
- Runtime de track de pessoa baseado em ROI, com tempo acumulado e confiança.
- Criação de evento de permanência com lógica de cooldown.
- Snapshot de saúde da câmera baseado na idade do último frame.
- Snapshot SVG sintético para screenshots e demonstrações públicas.

## Arquitetura

```text
frame da câmera -> detecção de pessoa -> track em ROI -> regra de permanência -> evento operacional
                                      -> snapshot de runtime -> endpoint de saúde
```

## Rodar Localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8013
```

Abra:

- `http://127.0.0.1:8013/`
- `http://127.0.0.1:8013/api/sidewalk/cameras`
- `http://127.0.0.1:8013/api/demo/sidewalk-camera/snapshot.svg`

Crie um evento sintético:

```bash
curl -X POST http://127.0.0.1:8013/api/demo/sidewalk-dwell
curl http://127.0.0.1:8013/api/sidewalk/events
```

## Escopo Público e Seguro

Todos os nomes de câmeras, sites, detecções, tracks e eventos são sintéticos. O repositório não inclui gravações de produção, IPs privados, credenciais de DVR/NVR, identificadores de clientes, SDKs proprietários ou destinos de alerta.

## Competências Representadas

Python, FastAPI, modelagem de domínio de video analytics, arquitetura orientada a OpenCV/YOLO, health checks de runtime, desenho de eventos para operação e visão prática de segurança eletrônica.
