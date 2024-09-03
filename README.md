# resolve-hostname-by-icmp
Service to resolve hostname by using SNMP to get the hostname of the ICMP source IP


Para rodar o script como um serviço no Ubuntu, você pode usar o systemd, que é o sistema de inicialização padrão. Aqui está um guia 

Passo a 
Passo para configurar o script como um serviço.


Passo 1: Colocar o Script na Pasta Desejada
Primeiro, coloque o script no diretório /opt/resolve-hostname-by-icmp/. Supondo que o nome do script seja resolve-hostname-by-icmp.py, o caminho completo seria:

/opt/resolve-hostname-by-icmp/resolve-hostname-by-icmp.py


Passo 2: Tornar o Script Executável
Certifique-se de que o script tenha permissões de execução. Você pode fazer isso com o seguinte comando:

sudo chmod +x /opt/resolve-hostname-by-icmp/resolve-hostname-by-icmp.py


Passo 3: Criar um Arquivo de Serviço Systemd
Agora, crie um arquivo de serviço systemd para gerenciar o script. Esse arquivo deve ser criado em /etc/systemd/system/.

Crie o arquivo de serviço com o comando:

sudo nano /etc/systemd/system/resolve-hostname-by-icmp.service


Passo 4: Configurar o Arquivo de Serviço
No editor de texto, adicione o seguinte conteúdo ao arquivo de serviço:

[Unit]
Description=Resolve Hostname by ICMP Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/resolve-hostname-by-icmp/resolve-hostname-by-icmp.py
WorkingDirectory=/opt/resolve-hostname-by-icmp/
Restart=always
User=root

[Install]
WantedBy=multi-user.target
Explicação dos Campos:
[Unit]

Description: Descrição do serviço.
After: Garante que o serviço só inicie após o sistema de rede estar disponível.
[Service]

ExecStart: Especifica o comando que será executado para iniciar o script.
WorkingDirectory: Define o diretório de trabalho do serviço.
Restart: Garante que o serviço será reiniciado automaticamente em caso de falha.
User: Define o usuário sob o qual o serviço será executado. Neste caso, root é necessário para atualizar o /etc/hosts.
[Install]

WantedBy: Define que o serviço deve ser iniciado no modo multiusuário (padrão para servidores).

Passo 5: Carregar o Novo Serviço
Depois de criar o arquivo de serviço, carregue o systemd para reconhecer o novo serviço:

sudo systemctl daemon-reload


Passo 6: Iniciar o Serviço
Agora, você pode iniciar o serviço usando o seguinte comando:

sudo systemctl start resolve-hostname-by-icmp.service


Passo 7: Habilitar o Serviço no Boot
Para garantir que o serviço seja iniciado automaticamente na inicialização do sistema, use o comando:

sudo systemctl enable resolve-hostname-by-icmp.service


Passo 8: Verificar o Status do Serviço
Para verificar se o serviço está rodando corretamente, use:

sudo systemctl status resolve-hostname-by-icmp.service


Passo 9: Monitorar Logs
Você pode visualizar os logs gerados pelo serviço com o comando:

sudo journalctl -u resolve-hostname-by-icmp.service
