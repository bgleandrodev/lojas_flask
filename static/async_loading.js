/* ============================================
   SATURNTECH - SISTEMA DE GESTÃO DE PRODUTOS
   Scripts de carregamento assíncrono e melhorias
   ============================================ */

// Aguarda o DOM completamente carregado antes de executar
document.addEventListener('DOMContentLoaded', function() {
    
    // Adiciona classe 'loaded' ao body para animação suave
    document.body.classList.add('loaded');
    
    // Log de inicialização no console (útil para debug)
    console.log('🚀 SaturnTech - Sistema de Gestão de Produtos carregado com sucesso!');
    console.log(`📅 Data/Hora: ${new Date().toLocaleString('pt-BR')}`);
    
    // Atualiza automaticamente o ano atual no footer se existir um elemento com a classe 'ano-atual'
    const anoElement = document.querySelector('.ano-atual');
    if (anoElement) {
        anoElement.textContent = new Date().getFullYear();
    }
    
    // Adiciona tooltips dinâmicos para tabelas (opcional)
    addTableTooltips();
    
    // Inicializa melhorias para dispositivos móveis
    initMobileImprovements();
    
    // Adiciona evento de clique nos cards para feedback visual
    initCardInteractions();
    
    // Carrega estatísticas dinâmicas (se necessário no futuro)
    loadDynamicStats();
});

/**
 * Detecta se o dispositivo é móvel
 * @returns {boolean} Verdadeiro se for dispositivo móvel
 */
function isMobileDevice() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
}

/**
 * Adiciona tooltips aos cabeçalhos das tabelas para explicar as colunas
 */
function addTableTooltips() {
    const tableHeaders = document.querySelectorAll('th');
    const tooltips = {
        'ID': 'Identificador único do produto',
        'Nome': 'Nome completo do produto',
        'Preço': 'Valor do produto em Reais (R$)',
        'Categoria': 'Classificação do produto',
        'Estoque': 'Quantidade disponível em estoque',
        'Produto': 'Nome do produto',
        'Média de Preço': 'Valor médio dos produtos nesta categoria',
        'Quantidade': 'Número de itens nesta categoria'
    };
    
    tableHeaders.forEach(header => {
        const text = header.textContent.trim();
        if (tooltips[text]) {
            header.title = tooltips[text];
            header.style.cursor = 'help';
        }
    });
}

/**
 * Inicializa melhorias específicas para dispositivos móveis
 */
function initMobileImprovements() {
    if (isMobileDevice()) {
        console.log('📱 Dispositivo móvel detectado - layout responsivo ativado');
        document.body.classList.add('mobile-view');
        
        // Adiciona botão de "rolar para o topo" em telas pequenas
        addScrollToTopButton();
        
        // Melhora a experiência de rolagem em tabelas
        improveTableScrolling();
    }
}

/**
 * Adiciona um botão flutuante para voltar ao topo da página
 */
function addScrollToTopButton() {
    // Verifica se o botão já existe
    if (document.querySelector('.scroll-top-btn')) return;
    
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '⬆️';
    scrollBtn.className = 'scroll-top-btn';
    scrollBtn.title = 'Voltar ao topo';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 24px;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s, visibility 0.3s;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    document.body.appendChild(scrollBtn);
    
    // Mostra/esconde o botão baseado no scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });
}

/**
 * Melhora a experiência de rolagem em tabelas em dispositivos móveis
 */
function improveTableScrolling() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.style.overflowX = 'auto';
        wrapper.style.webkitOverflowScrolling = 'touch';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

/**
 * Inicializa interações dos cards (feedback visual)
 */
function initCardInteractions() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });
}

/**
 * Carrega estatísticas dinâmicas via API (exemplo para expansão futura)
 */
async function loadDynamicStats() {
    try {
        // Exemplo: futuramente você pode carregar dados da API
        // const response = await fetch('/api/produtos');
        // const produtos = await response.json();
        // console.log(`📊 Total de produtos disponíveis: ${produtos.length}`);
        
        // Placeholder para futuras implementações
        console.log('📊 Sistema pronto para carregar estatísticas dinâmicas');
    } catch (error) {
        console.error('❌ Erro ao carregar estatísticas:', error);
    }
}

/**
 * Função utilitária para formatar moeda (caso precise no futuro)
 * @param {number} value - Valor a ser formatado
 * @returns {string} Valor formatado em R$
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Função utilitária para formatar data (caso precise no futuro)
 * @param {Date} date - Data a ser formatada
 * @returns {string} Data formatada
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(date);
}

// Exporta funções para uso global (se necessário)
window.SaturnTech = {
    isMobile: isMobileDevice,
    formatCurrency: formatCurrency,
    formatDate: formatDate
};