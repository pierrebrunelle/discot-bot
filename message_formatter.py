# message_formatter.py
import discord
from datetime import datetime
from typing import List, Dict

class MessageFormatter:
    """Helper class for consistent Discord message formatting"""

    # Discord color constants
    BLUE = discord.Color.blue()
    GREEN = discord.Color.green() 
    RED = discord.Color.red()

    @staticmethod
    def create_chat_embed(question: str, response: str, context: List[Dict]) -> discord.Embed:
        """Create formatted embed for chat responses with context"""
        embed = discord.Embed(
            title="💬 Chat Response",
            description=response,
            color=MessageFormatter.GREEN,
            timestamp=datetime.utcnow()
        )

        # Add question field (truncate if needed)
        embed.add_field(
            name="❓ Question",
            value=question[:1024],  # Discord field value limit
            inline=False
        )

        # Add relevant context field
        if context:
            context_text = []
            total_length = 0
            
            for i, ctx in enumerate(context, 1):
                score = round(float(ctx['sim']) * 100, 1)
                sender = ctx.get('username', 'Bot' if ctx.get('is_bot', False) else 'User')
                
                # Format context entry
                entry = (
                    f"{i}. {sender} ({score}% relevance)\n"
                    f"```{ctx['text'][:100]}```"  # Limit each context entry to 100 chars
                )
                
                # Check if adding this entry would exceed Discord's limit
                if total_length + len(entry) + 1 > 1024:  # +1 for newline
                    context_text.append("...")  # Add ellipsis to indicate truncation
                    break
                    
                context_text.append(entry)
                total_length += len(entry) + 1  # +1 for newline

            context_value = "\n".join(context_text) if context_text else "No relevant context found"
            
            embed.add_field(
                name="🧠 Relevant Context",
                value=context_value[:1024],  # Ensure we don't exceed Discord's limit
                inline=False
            )

        return embed

    @staticmethod
    def create_search_embed(results: List[Dict], query: str) -> discord.Embed:
        """Create formatted embed for search results"""
        embed = discord.Embed(
            title=f"🔍 Search Results for: {query[:100]}",  # Limit query length in title
            color=MessageFormatter.BLUE,
            timestamp=datetime.utcnow()
        )

        total_length = 0
        for i, result in enumerate(results, 1):
            # Format relevance score
            score = round(float(result['similarity']) * 100, 1)
            
            # Format message content
            sender = result.get('username', 'User')
            content = result['text'][:100]  # Limit content length
            
            # Create field content
            field_content = f"From: {sender}\n```{content}```"
            
            # Check total length
            if total_length + len(field_content) > 5000:  # Discord's total embed limit
                embed.add_field(
                    name="⚠️ Note",
                    value="Some results were truncated...",
                    inline=False
                )
                break
                
            embed.add_field(
                name=f"Result {i} ({score}% match)",
                value=field_content,
                inline=False
            )
            total_length += len(field_content)

        embed.set_footer(text=f"Found {len(results)} results")
        return embed

    @staticmethod
    def create_error_embed(error: str) -> discord.Embed:
        """Create formatted embed for errors"""
        embed = discord.Embed(
            title="Error Occurred",
            description=f"```{error}```",
            color=MessageFormatter.RED,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Please try again or contact support if the issue persists")
        return embed