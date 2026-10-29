# Exportação de memórias do Claude — Silvio

Exportado em 29/10/2026, após a limpeza. Conteúdo literal dos arquivos de memória, sem os cabeçalhos técnicos.

---

## Perfil

- Nome: Silvio
- Sócio da Vexta (vexta.com.br), não apenas funcionário
- Função híbrida entre engenharia de software e direito fiscal/tributário brasileiro
- Trabalha no ERP Vexta, baseado em SQL Server, que atende segmentos especializados como confecção e facção de costura
- Integrações profundas com sistemas fiscais brasileiros: NF-e, CT-e, GNRE, DF-e, SEFAZ
- Tem responsabilidades de infraestrutura e DevOps além do trabalho de produto e desenvolvimento
- CNAE principal da Vexta: 6203-1/00 (desenvolvimento e licenciamento de programas de computador não-customizáveis)
- CNAEs secundários da Vexta: 6209-1/00 (suporte técnico, manutenção e outros serviços em TI) e 6202-3/00 (desenvolvimento e licenciamento de programas de computador customizáveis)

## Preferências

- Entregar todos os documentos em Markdown por padrão; trocar de formato (ex.: .docx) só se pedido explicitamente
- Atuar como conselheiro estratégico direto e crítico: analisar ideias criticamente antes de concordar, evitar validação automática ou elogio genérico, apontar fraquezas, riscos e pontos cegos
- Nomear claramente quando Silvio parecer estar evitando algo desconfortável; priorizar feedback honesto e direto em vez de conforto

---

## Pessoas

### Guilherme
- Guilherme é filho de Silvio; o grupo familiar é só os dois (Silvio e Guilherme)

---

## Áreas ativas

### Efitex
- Efitex é um sistema com site feito no Lovable (efitex.lovable.app); Silvio está preparando um briefing (especificações, design, logo e marcas) para passar ao Claude Design criar o design do sistema
- Escopo do design no Claude Design: o app completo (não só a landing); não possui os arquivos-fonte originais do logo (SVG)
- Decisões de produto: aceita somente certificado A1; quem recusa a guarda do certificado não pode contratar; confecção e contador são parceiros que indicam e não têm perfil no app (a confecção pode pagar a assinatura da facção); DANFE enviado por e-mail por padrão, com opção de compartilhar; cores de status aprovadas (verde para sucesso, laranja para alerta, vermelho para erro); campos fiscais da tela de conferência ainda a definir
- Design system do Efitex no Claude Design cobre somente o app (sem landing); cancelar um retorno NÃO devolve a franquia de notas e o app precisa de tela para cancelar o retorno

### Vexta Vistoria
- Frontend acessível em https://vist.vexta.com.br/vistoria
- Ainda não existe identidade visual oficial definida para o projeto
- Planeja usar o Claude Design para propor a UX das telas existentes (não criar telas novas), seguindo diretrizes padrão de UI/UX para iOS/Android
- Stack do frontend: React 19, Vite 6, Material UI 7 (`@mui/material` + `@emotion`), React Router 7, Axios, `crypto-js`, `clientjs` (device fingerprint), `moment-timezone`, TypeScript
- Sistema de vistorias de remessas de fabricação, multi-tenant por subdomínio (cada empresa/tenant tem sua própria conexão SQL Server); agentes de campo registram vistorias e capturam fotos geolocalizadas vinculadas aos dados de produção do ERP
- Monorepo pnpm: backend em Node.js/Express/TypeScript com Sequelize (SQL Server); frontend SPA em React 19/Vite/MUI 7, servida sob o subpath /vistoria/
- Rotas do frontend: Login, Dashboard (boas-vindas), Vistorias (lista de remessas + modais de detalhe e registro de vistoria), BootError (falha de configuração de tenant)
- Geolocalização é obrigatória para o funcionamento do sistema (bloqueia a tela de boas-vindas se negada)
- Na tabela de remessas, o ícone de status por cor indica: verde = remessa já vistoriada, magenta/rosa = remessa ainda sem vistoria

### Sistema de restauração de backup
- Sistema interno web para executar restauração de backup em servidor SQL Server de teste/dev interno, relacionado ao servidor Ubuntu
- Arquivos de backup ficam armazenados num bucket S3; usuário escolhe qual baixar
- Cada ZIP no S3 contém dois BDs: um Mestre*.bak e um ERP*.bak, ambos devem ser restaurados
- Servidor de BD roda em Ubuntu 24 Linux; a aplicação Node vai rodar no mesmo host do SQL Server
- Pasta de download/descompactação dos backups: /home/vexta/baks
- Arquivos de log de BD restaurados vão para /mnt/dblog; arquivos de dados vão para /mnt/dbdata
- Após restaurar, é necessário atualizar as views do BD ERP* que referenciam o BD Mestre*, apontando para o Mestre correto recém-restaurado
- Acesso ao sistema via login Google, restrito ao domínio vexta.com.br
- Nome dos BDs restaurados varia conforme o arquivo baixado (ex.: AlfaCouros_DB_20260807_225000.zip gera MestreAlfaCouros e ERPAlfaCouros)
- Restauração pode sobrescrever BD existente, mediante confirmação do usuário
- Sistema precisa controlar concorrência entre restaurações
- Stack sugerida: NodeJS, padrão já utilizado pela empresa
- Concorrência: uma única restauração por vez no servidor (lock global)
- Nome do banco restaurado vem do nome do arquivo .bak dentro do ZIP (sem necessidade de derivar do nome do ZIP)
- Atualização das views do ERP referentes ao Mestre é feita via ALTER VIEW
- Confirmação de sobrescrita de BD existente: um "Tem certeza?" simples é suficiente
- Se o BD será sobrescrito, o sistema deve matar (kill) as conexões ativas antes de restaurar
- Limpeza de bancos de clientes antigos no servidor é manual, não automatizada pelo sistema
- ZIP e .bak envolvidos numa restauração devem ser apagados automaticamente ao final do processo
- Views do ERP que referenciam o Mestre são identificadas por um marcador `/*BancoMestre*/` no código antes do nome do banco (ex.: `/*BancoMestre*/MestreXpto.dbo.PARAMETRO`); a atualização troca o nome do banco logo após esse marcador

### Servidor interno Ubuntu / SQL Server DEV
- Servidor Ubuntu 24.04 Server com SQL Server 2025 para uso interno da empresa (ambientes DEV e Tester), não é um teste descartável
- 3 HDs: SO num disco, dados e backup nos outros dois (500GB e 2TB); 16GB de RAM
- IP fixo 192.168.30.50/24 na interface enp2s0 via netplan (gateway 192.168.30.254, DHCP da rede 192.168.30.250), com gerenciamento de rede do cloud-init desativado
- Monitoramento de espaço em disco via Uptime Kuma (push monitors) em vez de rotina T-SQL, por bloqueio de xp_cmdshell na edição do SQL Server instalada

### Monitoramento de normas SEFAZ
- Analisa normas fiscais (ex.: NT 2026.007, NT 2026.002) no contexto de facção/confecção, em análises de impacto de seis seções com especificação de implementação no ERP
- Templates de prompt reutilizáveis para monitorar publicações da SEFAZ (Notas Técnicas, ajustes SINIEF) via Hermes Agent com estado persistente
- Status do monitoramento via Hermes Agent: amadurecendo (out/2026)

### Renda extra online
- Tempo disponível: poucas horas por semana (renda complementar, não segundo emprego)
- Tolerância a risco baixa, prefere algo previsível
- Precisa gerar caixa em até 3 meses
- Restrições: não pode vender curso, não quer depender de tráfego pago
- Já tem em andamento um SaaS de SEO local para pequenos negócios brasileiros, ainda em fase de validação sem receita — não é o foco desta busca, quer algo adicional/alternativo; busca e SaaS seguem existindo (out/2026)
- Consegue obter anuência dos demais sócios da Vexta para atividade paralela, mas mesmo assim decidiu descartar a ideia de consultoria pontual SQL Server/infraestrutura
- Descartou ideias de monitoramento de normas SEFAZ e de integrador fiscal (NF-e/CT-e) por conflito com dever de lealdade societária, sendo sócio da Vexta
- Descartou ideia de automação/RPA para PMEs por não ter rede de contatos (partiria do zero), incompatível com prazo de caixa em 3 meses
- Não quer usar SQL Server especificamente para gerar renda extra, mas desenvolvimento em geral está aberto

### Sítio em Atalanta
- Possui um sítio no interior de Atalanta (SC), em condomínio rural com mais 2 CPFs (copropriedade)
- Construção de galpão 6x8 (garagem/área de festas); em set/2026 a previsão era ficar pronto em cerca de 6 meses

---

## Áreas paradas

### AppDoRepresentante — migração
- Migração planejada do AppDoRepresentante de Ionic v1/AngularJS para Ionic + Angular + Capacitor, com abordagem documentation-first usando Claude Code
- Emulador do Android Studio numa máquina Ubuntu com pouco recurso; RAM e GPU eram os principais bloqueios
- Status: parado (out/2026)

### Integração TEF/PayGo
- Integração TEF/PayGo em Node.js/Express para o ERP Vexta: wrapper completo com gestão idempotente de transações e retry, mais orientação de arquitetura para PinPad
- Status: parado (out/2026)

### Guarda legal
- Projetou um serviço multi-tenant de guarda legal de documentos fiscais NF-e/CT-e
- Object storage compatível com S3 e indexação de metadados em SQL Server; acesso de clientes isolado por JWT
- Status: parado (out/2026)

### Gerenciador web de SQL Server
- Definição de requisitos de um sistema web de gestão de SQL Server para substituir o SSMS internamente na Vexta
- Escopo: modelo de catálogo, isolamento de autenticação, desenho de log de auditoria; inclui avaliação build-vs-buy contra o CloudBeaver Enterprise
- Status: parado (out/2026)

---

## Tópicos

### Energia solar
- É micro produtor de energia solar (geração distribuída/net metering)

### Infraestrutura
- Interesse recorrente em configuração de Nginx (keepalive de upstream, timeouts de proxy)
- Interesse recorrente em arquitetura de backend Node.js

### DIY
- Interesse em projetos mão na massa (DIY)
- Projeto de motosserra de bancada (caseira) com cálculos de transmissão mecânica
