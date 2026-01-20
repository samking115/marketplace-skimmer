"""
Value analyzer module.
Compares marketplace prices to eBay sold prices to identify undervalued items.
"""
from typing import Dict, Optional, List


class ValueAnalyzer:
    """Analyzer for comparing marketplace prices to eBay sold prices."""
    
    def __init__(self, config: dict):
        self.config = config
        self.threshold = config['analysis']['undervalued_threshold_percent']
        
    def analyze_item(self, marketplace_item: Dict, ebay_stats: Optional[Dict]) -> Optional[Dict]:
        """
        Analyze if a marketplace item is undervalued compared to eBay.
        
        Args:
            marketplace_item: Item from Facebook Marketplace
            ebay_stats: Price statistics from eBay sold listings
            
        Returns:
            Analysis result with value assessment, or None if not undervalued
        """
        if not ebay_stats:
            print(f"[INFO] Skipping '{marketplace_item['title']}' - no eBay data")
            return None
        
        marketplace_price = marketplace_item['price']
        ebay_avg_price = ebay_stats['average']
        ebay_median_price = ebay_stats['median']
        
        # Calculate discount percentage
        discount_from_avg = ((ebay_avg_price - marketplace_price) / ebay_avg_price) * 100
        discount_from_median = ((ebay_median_price - marketplace_price) / ebay_median_price) * 100
        
        # Determine if undervalued
        is_undervalued = discount_from_avg >= self.threshold
        
        analysis = {
            'marketplace_item': marketplace_item,
            'marketplace_price': marketplace_price,
            'ebay_average': ebay_avg_price,
            'ebay_median': ebay_median_price,
            'ebay_min': ebay_stats['min'],
            'ebay_max': ebay_stats['max'],
            'ebay_sample_count': ebay_stats['count'],
            'discount_percent_avg': discount_from_avg,
            'discount_percent_median': discount_from_median,
            'potential_profit': ebay_avg_price - marketplace_price,
            'is_undervalued': is_undervalued,
            'confidence': self._calculate_confidence(ebay_stats)
        }
        
        if is_undervalued:
            print(f"[✓] UNDERVALUED: '{marketplace_item['title']}'")
            print(f"    Marketplace: ${marketplace_price:.2f} | eBay Avg: ${ebay_avg_price:.2f}")
            print(f"    Discount: {discount_from_avg:.1f}% | Potential Profit: ${analysis['potential_profit']:.2f}")
            return analysis
        else:
            print(f"[✗] Not undervalued: '{marketplace_item['title']}' ({discount_from_avg:.1f}% discount)")
            return None
    
    def _calculate_confidence(self, ebay_stats: Dict) -> str:
        """
        Calculate confidence level based on eBay sample size and price variance.
        
        Args:
            ebay_stats: eBay price statistics
            
        Returns:
            Confidence level: 'high', 'medium', or 'low'
        """
        sample_count = ebay_stats['count']
        price_range = ebay_stats['max'] - ebay_stats['min']
        price_avg = ebay_stats['average']
        
        # Calculate coefficient of variation
        variance_ratio = price_range / price_avg if price_avg > 0 else 1.0
        
        # Determine confidence
        if sample_count >= 10 and variance_ratio < 0.3:
            return 'high'
        elif sample_count >= 5 and variance_ratio < 0.5:
            return 'medium'
        else:
            return 'low'
    
    def rank_opportunities(self, analyses: List[Dict]) -> List[Dict]:
        """
        Rank undervalued items by best opportunities.
        
        Args:
            analyses: List of analysis results
            
        Returns:
            Sorted list of opportunities (best first)
        """
        # Filter only undervalued items
        undervalued = [a for a in analyses if a and a['is_undervalued']]
        
        # Sort by potential profit (descending)
        ranked = sorted(undervalued, key=lambda x: x['potential_profit'], reverse=True)
        
        return ranked
