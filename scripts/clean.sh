#!/bin/bash
################################################################################
# Script de Nettoyage
# Supprime tous les conteneurs, volumes et données
################################################################################

echo "=========================================="
echo "🧹 NETTOYAGE COMPLET"
echo "=========================================="
echo ""
echo "⚠️  ATTENTION: Cette opération va supprimer:"
echo "   - Tous les conteneurs Docker"
echo "   - Tous les volumes (données HDFS, MongoDB)"
echo "   - Les checkpoints Spark"
echo ""
read -p "Êtes-vous sûr? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Nettoyage annulé"
    exit 0
fi

echo ""
echo "🗑️  Suppression des conteneurs et volumes..."
docker-compose down -v

echo ""
echo "🗑️  Nettoyage des checkpoints..."
rm -rf /tmp/spark-checkpoint-*

echo ""
echo "✅ Nettoyage terminé"
echo ""
echo "Pour redémarrer à zéro:"
echo "  1. ./scripts/setup.sh"
echo "  2. docker-compose up -d"
echo "  3. ./scripts/prepare_hdfs.sh"
echo ""
