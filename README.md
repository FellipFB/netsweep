# NetSweep

NetSweep é uma ferramenta de varredura de rede local e análise de serviços, escrita em Python. Ideal para administradores de rede, estudantes de segurança e curiosos que querem descobrir quais dispositivos estão conectados na sua rede e quais serviços eles estão rodando.

## Funcionalidades

- **ARP Scan**: Descobre todos os dispositivos na rede local (IP, MAC, hostname, fabricante)
- **Port Scan**: Escaneia portas comuns em cada dispositivo encontrado
- **Relatórios**: Gera relatórios em HTML (bonito) ou CSV (para planilhas)
- **Interface CLI simples e bonita** com Rich

## Instalação

```bash
git clone https://github.com/FellipFB/netsweep.git
cd netsweep
pip install -r requirements.txt
pip install -e .
```
