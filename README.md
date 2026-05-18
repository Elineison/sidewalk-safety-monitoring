# Sidewalk Safety Monitoring

Módulo FastAPI que representa monitoramento de permanência em calçadas usando câmeras, ROI e tracks de pessoas dentro de uma operação VMS.

## O Que Significa VMS Aqui

VMS significa Sistema de Gerenciamento de Vídeo: a camada que centraliza câmeras, DVRs/NVRs, streams ao vivo, gravações, eventos, alertas e integrações. Neste repositório, o VMS é a base operacional que fornece vídeo em tempo real e recebe eventos, runtime e health checks do módulo.

## O Que o Sistema Faz

- Recebe detecções sintéticas vindas de um worker de vídeo em tempo real conectado ao VMS.
- Mantém runtime por câmera com último frame, tracks ativos, ROI e cooldown.
- Gera evento quando uma pessoa permanece na ROI da calçada acima do limite configurado.
- Expõe snapshot SVG sintético para demonstrar a ideia de ROI e track sem usar imagem real.
- Expõe health check para identificar câmera sem frames recentes.

## Contexto Representado

- Câmeras em operação VMS com família Dahua/Intelbras.
- Worker de stream em tempo real alimentando o módulo de analytics.
- Integração entre detecção, runtime, eventos e suporte operacional.

## Endpoints

- `GET /` - página simples com links do módulo.
- `GET /api/sidewalk/cameras` - câmeras configuradas e runtime.
- `GET /api/sidewalk/cameras/{camera_id}/runtime` - runtime de uma câmera.
- `POST /api/sidewalk/cameras/{camera_id}/detections` - ingere uma detecção sintética.
- `POST /api/demo/sidewalk-dwell` - cria evento sintético de permanência.
- `GET /api/sidewalk/events` - lista eventos gerados.
- `GET /api/system/health` - saúde do módulo.
- `GET /api/demo/sidewalk-camera/snapshot.svg` - evidência visual sintética.

## Rodar Localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8013
```

## Testar

```bash
curl http://127.0.0.1:8013/api/sidewalk/cameras
curl -X POST http://127.0.0.1:8013/api/demo/sidewalk-dwell
curl http://127.0.0.1:8013/api/sidewalk/events
curl http://127.0.0.1:8013/api/system/health
```

Abra no navegador:

```text
http://127.0.0.1:8013/api/demo/sidewalk-camera/snapshot.svg
```

## Escopo Público

Todos os dados são sintéticos. Não há imagens reais, gravações, IPs privados, credenciais, SDKs proprietários, nomes de clientes ou endpoints reais de alerta.
