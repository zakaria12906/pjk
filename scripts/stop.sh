#!/bin/bash
################################################################################
# Script d'Arrêt des Services
# Arrête proprement tous les conteneurs Docker
################################################################################

echo "=========================================="
echo "🛑 ARRÊT DES SERVICES"
echo "=========================================="
echo ""

# Arrêter les conteneurs
echo "⏸️  Arrêt des conteneurs..."
docker-compose down

echo ""
echo "✅ Services arrêtés"
echo ""
echo "Pour redémarrer: docker-compose up -d"
echo ""
