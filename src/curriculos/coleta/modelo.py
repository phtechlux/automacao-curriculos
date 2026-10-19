import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Vaga:
    titulo: str
    link: str
    fonte: str
    empresa: str = ""
    local: str = ""
    descricao: str = ""
    status: str = "nova"  # nova | gerada | candidatada | descartada
    pdf: str = ""
    analise: dict = field(default_factory=dict)  # cobertura, requisitos, lacunas, entrevista

    @property
    def id(self) -> str:
        return hashlib.sha1(self.link.encode()).hexdigest()[:12]

    def salvar(self, pasta: Path) -> Path:
        pasta.mkdir(parents=True, exist_ok=True)
        caminho = pasta / f"{self.fonte}_{self.id}.json"
        caminho.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")
        return caminho

    @classmethod
    def carregar(cls, caminho: Path) -> "Vaga":
        return cls(**json.loads(caminho.read_text(encoding="utf-8")))
