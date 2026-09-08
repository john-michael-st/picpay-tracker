# PicPay Tracker - Frontend

Este é o frontend PWA do aplicativo PicPay Tracker, desenvolvido em React + Vite.

## Como instalar e rodar localmente

1. Certifique-se de ter o Node.js instalado (v18+).
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Rode o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
4. Acesse `http://localhost:5173` no navegador.

## Como fazer o deploy na Vercel

1. Crie uma conta no [Vercel](https://vercel.com).
2. Você pode conectar seu repositório GitHub e importar o projeto, escolhendo a pasta `frontend`. O Vercel detectará automaticamente que é um app Vite.
3. **Alternativa Manual (Drag & Drop):**
   - Rode `npm run build` localmente para gerar a pasta `dist/`.
   - Arraste a pasta `dist/` gerada para a página principal da sua dashboard no Vercel.

## Decisões Técnicas

- **PWA**: Utilizado o plugin `vite-plugin-pwa` para gerar automaticamente o Service Worker e manifest.json. O app é instalável e guarda cache local de forma básica para ser aberto offline.
- **Armazenamento de Configurações**: URL da API e Token são salvos no `localStorage` do dispositivo. Isso facilita o deploy do frontend (não precisa de .env no build) e permite usar a mesma interface conectando a backends diferentes, caso desejado.
- **Estilização**: Uso de CSS Vanilla com Variáveis (CSS Variables) seguindo um padrão mobile-first. Permite manter o pacote enxuto sem depender de bibliotecas de UI pesadas (Tailwind, MUI), garantindo um carregamento mais rápido no PWA.
- **Hooks customizados**: `useResumo.js` foi criado para implementar um polling (30s) que atualiza os dados na tela Dashboard automaticamente.
