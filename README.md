# scopenet

Socket based client-server message controller, designed as a prototype for telescope mount control

Para usar a aplicação:

- Abra um terminal no local do projeto (./scopenet)
- Execute um servidor observatório.

````shell
python scope-server.py
````

Noutro terminal, simule uma sessão de um cliente:

````shell
python scope-client.py
````

Uma interface deve aparecer agora, onde é possível inserir instruções para o observatório. Também é possível
abrir mais de uma sessão cliente para controlar o observatório.

Há dois comandos disponíveis: 
- `GoTo` envia o telescópio para a posição sideral desejada.
- `Track` Inicia o acompanhamento do alvo atual.

Caso deseje criar uma seção entre computadores numa rede local, altere o endereço do `HOST` encontrado nos arquivos
acima executados.