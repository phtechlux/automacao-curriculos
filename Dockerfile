# Fase 7 (HOS-02): imagem com Playwright/Chromium já instalado, pronta pra gerar PDF hospedado.
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e .

COPY templates ./templates
COPY prompts ./prompts
COPY data/curriculo_base/curriculo.exemplo.yaml data/curriculo_base/
COPY data/vagas/.gitkeep data/vagas/
COPY output/.gitkeep output/

# data/contas (créditos/currículo/vagas por cliente) é gravado em runtime: monte um
# volume persistente nesse caminho — sem isso, cada deploy apaga os clientes (HOS-01/HOS-02).
ENV HOST=0.0.0.0
ENV PORTA=8765
EXPOSE 8765

CMD ["python", "-m", "curriculos", "painel"]
