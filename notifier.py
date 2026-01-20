"""
Notification module for alerting about undervalued items.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime


class Notifier:
    """Handles notifications for undervalued items."""
    
    def __init__(self, config: dict):
        self.config = config
        self.notification_config = config['notifications']
        
    def notify(self, opportunities: List[Dict]) -> None:
        """
        Send notifications about undervalued items.
        
        Args:
            opportunities: List of undervalued items (ranked)
        """
        if not opportunities:
            print("[INFO] No undervalued items found - no notifications to send")
            return
        
        print(f"\n{'='*80}")
        print(f"Found {len(opportunities)} undervalued item(s)!")
        print(f"{'='*80}\n")
        
        # Console notification (always enabled by default)
        if self.notification_config.get('console', True):
            self._notify_console(opportunities)
        
        # Email notification (if enabled)
        if self.notification_config.get('email', False):
            self._notify_email(opportunities)
    
    def _notify_console(self, opportunities: List[Dict]) -> None:
        """Print notifications to console."""
        for i, opp in enumerate(opportunities, 1):
            item = opp['marketplace_item']
            
            print(f"{'─'*80}")
            print(f"🔥 OPPORTUNITY #{i} - Confidence: {opp['confidence'].upper()}")
            print(f"{'─'*80}")
            print(f"Title:       {item['title']}")
            print(f"Location:    {item['location']}")
            print(f"URL:         {item['url']}")
            print(f"\nPRICING:")
            print(f"  Marketplace Price:  ${opp['marketplace_price']:.2f}")
            print(f"  eBay Average:       ${opp['ebay_average']:.2f}")
            print(f"  eBay Median:        ${opp['ebay_median']:.2f}")
            print(f"  eBay Range:         ${opp['ebay_min']:.2f} - ${opp['ebay_max']:.2f}")
            print(f"\nVALUE ANALYSIS:")
            print(f"  Discount:           {opp['discount_percent_avg']:.1f}% below average")
            print(f"  Potential Profit:   ${opp['potential_profit']:.2f}")
            print(f"  eBay Samples:       {opp['ebay_sample_count']} sold listings")
            print(f"\nDESCRIPTION:")
            print(f"  {item['description'][:200]}...")
            print()
        
        print(f"{'='*80}\n")
    
    def _notify_email(self, opportunities: List[Dict]) -> None:
        """Send email notification."""
        email_address = self.notification_config.get('email_address')
        
        if not email_address:
            print("[WARN] Email notification enabled but no email address configured")
            return
        
        try:
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'🔥 {len(opportunities)} Undervalued Item(s) Found on Facebook Marketplace'
            msg['From'] = self.notification_config.get('smtp_username', 'marketplace-skimmer@localhost')
            msg['To'] = email_address
            
            # Create email body
            text_body = self._create_email_text(opportunities)
            html_body = self._create_email_html(opportunities)
            
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            smtp_server = self.notification_config.get('smtp_server')
            smtp_port = self.notification_config.get('smtp_port', 587)
            smtp_username = self.notification_config.get('smtp_username')
            smtp_password = self.notification_config.get('smtp_password')
            
            if not all([smtp_server, smtp_username, smtp_password]):
                print("[WARN] Email notification enabled but SMTP settings incomplete")
                return
            
            print(f"[INFO] Sending email notification to {email_address}...")
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            print("[INFO] Email notification sent successfully")
            
        except Exception as e:
            print(f"[ERROR] Failed to send email notification: {e}")
    
    def _create_email_text(self, opportunities: List[Dict]) -> str:
        """Create plain text email body."""
        lines = [
            f"Marketplace Skimmer Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"Found {len(opportunities)} undervalued item(s):",
            ""
        ]
        
        for i, opp in enumerate(opportunities, 1):
            item = opp['marketplace_item']
            lines.extend([
                f"#{i}. {item['title']}",
                f"   Price: ${opp['marketplace_price']:.2f} (eBay avg: ${opp['ebay_average']:.2f})",
                f"   Discount: {opp['discount_percent_avg']:.1f}% | Profit potential: ${opp['potential_profit']:.2f}",
                f"   URL: {item['url']}",
                ""
            ])
        
        return "\n".join(lines)
    
    def _create_email_html(self, opportunities: List[Dict]) -> str:
        """Create HTML email body."""
        html = [
            "<html>",
            "<head><style>",
            "body { font-family: Arial, sans-serif; }",
            "h1 { color: #1877f2; }",
            ".item { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }",
            ".item h3 { margin-top: 0; color: #333; }",
            ".price { font-size: 18px; font-weight: bold; color: #00a650; }",
            ".discount { color: #ff6b6b; font-weight: bold; }",
            "</style></head>",
            "<body>",
            f"<h1>🔥 {len(opportunities)} Undervalued Item(s) Found!</h1>",
            f"<p><em>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>",
        ]
        
        for i, opp in enumerate(opportunities, 1):
            item = opp['marketplace_item']
            html.extend([
                f"<div class='item'>",
                f"<h3>#{i}. {item['title']}</h3>",
                f"<p class='price'>Marketplace: ${opp['marketplace_price']:.2f} | eBay Avg: ${opp['ebay_average']:.2f}</p>",
                f"<p class='discount'>Discount: {opp['discount_percent_avg']:.1f}% | Potential Profit: ${opp['potential_profit']:.2f}</p>",
                f"<p><strong>Confidence:</strong> {opp['confidence'].title()}</p>",
                f"<p><strong>Location:</strong> {item['location']}</p>",
                f"<p><a href='{item['url']}'>View on Facebook Marketplace</a></p>",
                f"<p><small>{item['description'][:200]}...</small></p>",
                "</div>",
            ])
        
        html.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html)
