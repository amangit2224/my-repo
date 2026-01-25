import React from 'react';
import './MarkdownSummary.css'; // We'll create this file

const MarkdownSummary = ({ content }) => {
  /**
   * Parse markdown and convert to React elements
   * Handles: ## (h2), ### (h3), **bold**, regular text
   */
  const parseMarkdown = (text) => {
    if (!text) return [];

    const elements = [];
    const lines = text.split('\n');
    let key = 0;

    lines.forEach((line) => {
      if (!line.trim()) {
        // Empty line - add spacing
        elements.push(<div key={key} className="markdown-spacer" />);
        key++;
        return;
      }

      // Check for ### (h3) - must come before ## to avoid false matches
      if (line.startsWith('### ')) {
        const text = line.replace('### ', '').trim();
        const content = parseInlineMarkdown(text);
        elements.push(
          <h3 key={key} className="markdown-h3">
            {content}
          </h3>
        );
        key++;
      }
      // Check for ## (h2)
      else if (line.startsWith('## ')) {
        const text = line.replace('## ', '').trim();
        const content = parseInlineMarkdown(text);
        elements.push(
          <h2 key={key} className="markdown-h2">
            {content}
          </h2>
        );
        key++;
      }
      // Regular text with potential bold
      else {
        const text = line.trim();
        if (text) {
          const content = parseInlineMarkdown(text);
          elements.push(
            <p key={key} className="markdown-p">
              {content}
            </p>
          );
          key++;
        }
      }
    });

    return elements;
  };

  /**
   * Parse inline markdown: **bold**, remove *, →
   */
  const parseInlineMarkdown = (text) => {
    // Remove → arrows and stray *
    text = text.replace(/→/g, '→').replace(/\*(?!\*)/g, '');

    // Split by ** to find bold sections
    const parts = text.split(/\*\*(.+?)\*\*/);
    
    return parts.map((part, index) => {
      if (index % 2 === 1) {
        // This is bold content
        return <strong key={index}>{part}</strong>;
      }
      // Regular text
      return part;
    });
  };

  const elements = parseMarkdown(content);

  return (
    <div className="markdown-summary">
      {elements.length > 0 ? (
        elements
      ) : (
        <p className="markdown-p">No summary available</p>
      )}
    </div>
  );
};

export default MarkdownSummary;