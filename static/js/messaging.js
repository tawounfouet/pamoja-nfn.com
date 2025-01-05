class MessagingWidget {
    constructor(container) {
        this.container = container;
        this.conversationList = container.querySelector('.conversation-list');
        this.messageContainer = container.querySelector('.message-container');
        this.messageList = container.querySelector('[data-message-list]');
        this.messageForm = container.querySelector('[data-message-form]');
        this.messageTemplate = document.getElementById('messageTemplate');
        this.currentConversationId = null;
        this.typingTimeout = null;
        
        this.setupWebSocket();
        this.setupEventListeners();
    }

    setupWebSocket() {
        this.ws = new WebSocket(
            `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/messaging/`
        );

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };

        this.ws.onclose = () => {
            console.log('WebSocket connection closed');
            // Tentative de reconnexion après 5 secondes
            setTimeout(() => this.setupWebSocket(), 5000);
        };
    }

    setupEventListeners() {
        // Gestion des conversations
        this.conversationList.addEventListener('click', (e) => {
            const conversationItem = e.target.closest('.conversation-item');
            if (conversationItem) {
                this.loadConversation(conversationItem.dataset.conversationId);
            }
        });

        // Gestion du formulaire de message
        if (this.messageForm) {
            this.messageForm.addEventListener('submit', (e) => this.handleMessageSubmit(e));
            
            const textarea = this.messageForm.querySelector('textarea');
            textarea.addEventListener('input', () => {
                this.sendTypingStatus(true);
                clearTimeout(this.typingTimeout);
                this.typingTimeout = setTimeout(() => this.sendTypingStatus(false), 1000);
            });
        }

        // Gestion de la nouvelle conversation
        const newConversationBtn = this.container.querySelector('[data-new-conversation]');
        if (newConversationBtn) {
            newConversationBtn.addEventListener('click', () => this.showNewConversationModal());
        }

        // Retour à la liste des conversations
        const backButton = this.container.querySelector('.back-to-conversations');
        if (backButton) {
            backButton.addEventListener('click', () => this.showConversationList());
        }

        // Suppression de conversation
        const deleteButton = this.container.querySelector('[data-delete-conversation]');
        if (deleteButton) {
            deleteButton.addEventListener('click', () => this.handleConversationDelete());
        }
    }

    async loadConversation(conversationId) {
        try {
            const response = await fetch(`/api/messaging/conversations/${conversationId}/`);
            const data = await response.json();
            
            this.currentConversationId = conversationId;
            this.showMessageContainer();
            this.updateRecipientInfo(data.recipient);
            this.renderMessages(data.messages);
            
            // Marquer comme lu
            this.markConversationAsRead(conversationId);
        } catch (error) {
            console.error('Erreur lors du chargement de la conversation:', error);
        }
    }

    async handleMessageSubmit(e) {
        e.preventDefault();
        const textarea = this.messageForm.querySelector('textarea');
        const content = textarea.value.trim();
        
        if (!content) return;

        try {
            const response = await fetch(`/api/messaging/conversations/${this.currentConversationId}/messages/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ content })
            });

            if (response.ok) {
                const message = await response.json();
                this.addMessage(message);
                textarea.value = '';
                textarea.focus();
            }
        } catch (error) {
            console.error('Erreur lors de l\'envoi du message:', error);
        }
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'new_message':
                if (data.conversation_id === this.currentConversationId) {
                    this.addMessage(data.message);
                }
                this.updateConversationPreview(data);
                break;
            case 'typing_status':
                if (data.conversation_id === this.currentConversationId) {
                    this.updateTypingStatus(data.is_typing);
                }
                break;
            case 'message_read':
                this.updateMessageStatus(data);
                break;
        }
    }

    addMessage(message) {
        const messageElement = this.messageTemplate.content.cloneNode(true);
        const messageItem = messageElement.querySelector('.message-item');
        
        messageItem.classList.add(message.is_outgoing ? 'outgoing' : 'incoming');
        messageItem.querySelector('.message-text').textContent = message.content;
        messageItem.querySelector('.message-time').textContent = this.formatDate(message.created_at);
        
        this.messageList.appendChild(messageItem);
        this.scrollToBottom();
    }

    updateTypingStatus(isTyping) {
        const typingIndicator = this.container.querySelector('.typing-indicator');
        typingIndicator.classList.toggle('d-none', !isTyping);
    }

    sendTypingStatus(isTyping) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'typing_status',
                conversation_id: this.currentConversationId,
                is_typing: isTyping
            }));
        }
    }

    async markConversationAsRead(conversationId) {
        try {
            await fetch(`/api/messaging/conversations/${conversationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });
            
            const conversationItem = this.conversationList.querySelector(
                `[data-conversation-id="${conversationId}"]`
            );
            if (conversationItem) {
                conversationItem.classList.remove('unread');
            }
        } catch (error) {
            console.error('Erreur lors du marquage comme lu:', error);
        }
    }

    showMessageContainer() {
        this.conversationList.classList.add('d-none');
        this.messageContainer.classList.remove('d-none');
    }

    showConversationList() {
        this.messageContainer.classList.add('d-none');
        this.conversationList.classList.remove('d-none');
        this.currentConversationId = null;
    }

    scrollToBottom() {
        this.messageList.scrollTop = this.messageList.scrollHeight;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-messaging-widget]').forEach(container => {
        new MessagingWidget(container);
    });
}); 