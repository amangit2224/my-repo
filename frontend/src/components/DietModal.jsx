import React from 'react';
import '../App.css';

function DietModal({ isOpen, onClose, dietPlan, loading }) {
  if (!isOpen) return null;

  return (
    <div 
      className="modal-overlay"
      onClick={onClose}
    >
      <div 
        className="diet-modal-container"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="diet-modal-header">
          <div className="diet-header-content">
            <div className="diet-header-icon">
              <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
              </svg>
            </div>
            <div>
              <h2>Personalized Diet Plan</h2>
              <p>Based on your medical report analysis</p>
            </div>
          </div>
          <button onClick={onClose} className="diet-close-btn">
            <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"/>
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="diet-modal-content">
          {loading ? (
            <div className="diet-loading-state">
              <div className="loading-spinner"></div>
              <h3>Generating Your Diet Plan</h3>
              <p>Analyzing your medical data to create personalized recommendations...</p>
            </div>
          ) : dietPlan ? (
            <>
              {/* Conditions Detected */}
              {dietPlan.conditions_detected && dietPlan.conditions_detected.length > 0 && (
                <DietSection 
                  title="Health Conditions Detected"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                      <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                    </svg>
                  }
                  color="#F59E0B"
                >
                  <div className="condition-badges">
                    {dietPlan.conditions_detected.map((condition, idx) => (
                      <span key={idx} className="condition-badge">
                        {condition.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>
                </DietSection>
              )}

              {/* Dietary Goals */}
              {dietPlan.dietary_goals && dietPlan.dietary_goals.length > 0 && (
                <DietSection 
                  title="Your Dietary Goals"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                  }
                  color="#3B82F6"
                >
                  <ul className="diet-list">
                    {dietPlan.dietary_goals.map((goal, idx) => (
                      <li key={idx}>{goal}</li>
                    ))}
                  </ul>
                </DietSection>
              )}

              {/* Foods to Eat */}
              {dietPlan.foods_to_eat && Object.keys(dietPlan.foods_to_eat).length > 0 && (
                <DietSection 
                  title="Foods to Include"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                  }
                  color="#10B981"
                >
                  {Object.entries(dietPlan.foods_to_eat).map(([category, foods]) => (
                    foods && foods.length > 0 && (
                      <FoodCategory 
                        key={category} 
                        title={category.replace(/_/g, ' ')} 
                        foods={foods}
                        type="include"
                      />
                    )
                  ))}
                </DietSection>
              )}

              {/* Foods to Avoid */}
              {dietPlan.foods_to_avoid && Object.keys(dietPlan.foods_to_avoid).length > 0 && (
                <DietSection 
                  title="Foods to Avoid/Limit"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clipRule="evenodd"/>
                    </svg>
                  }
                  color="#EF4444"
                >
                  {Object.entries(dietPlan.foods_to_avoid).map(([riskLevel, foods]) => (
                    foods && foods.length > 0 && (
                      <FoodCategory 
                        key={riskLevel} 
                        title={riskLevel.replace(/_/g, ' ')} 
                        foods={foods}
                        type="avoid"
                      />
                    )
                  ))}
                </DietSection>
              )}

              {/* Meal Suggestions */}
              {dietPlan.meal_suggestions && Object.keys(dietPlan.meal_suggestions).length > 0 && (
                <DietSection 
                  title="Sample Meal Ideas"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd"/>
                    </svg>
                  }
                  color="#EC4899"
                >
                  <div className="meal-suggestions-grid">
                    {Object.entries(dietPlan.meal_suggestions).map(([mealTime, suggestions]) => (
                      suggestions && suggestions.length > 0 && (
                        <div key={mealTime} className="meal-time-card">
                          <h4>{mealTime.replace(/_/g, ' ')}</h4>
                          <ul>
                            {suggestions.map((suggestion, idx) => (
                              <li key={idx}>{suggestion}</li>
                            ))}
                          </ul>
                        </div>
                      )
                    ))}
                  </div>
                </DietSection>
              )}

              {/* Nutritional Targets */}
              {dietPlan.nutritional_targets && Object.keys(dietPlan.nutritional_targets).length > 0 && (
                <DietSection 
                  title="Nutritional Targets"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/>
                    </svg>
                  }
                  color="#6366F1"
                >
                  <div className="nutritional-targets-grid">
                    {Object.entries(dietPlan.nutritional_targets).map(([nutrient, target]) => (
                      <div key={nutrient} className="nutrient-card">
                        <div className="nutrient-label">{nutrient.replace(/_/g, ' ')}</div>
                        <div className="nutrient-value">{target}</div>
                      </div>
                    ))}
                  </div>
                </DietSection>
              )}

              {/* Lifestyle Tips */}
              {dietPlan.lifestyle_tips && dietPlan.lifestyle_tips.length > 0 && (
                <DietSection 
                  title="Lifestyle Tips"
                  icon={
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/>
                    </svg>
                  }
                  color="#F59E0B"
                >
                  <div className="lifestyle-tips-grid">
                    {dietPlan.lifestyle_tips.map((tip, idx) => (
                      <div key={idx} className="lifestyle-tip-card">
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                        </svg>
                        {tip}
                      </div>
                    ))}
                  </div>
                </DietSection>
              )}

              {/* General Notes */}
              {dietPlan.general_notes && dietPlan.general_notes.length > 0 && (
                <div className="diet-important-notes">
                  <div className="notes-header">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                    </svg>
                    <h3>Important Notes</h3>
                  </div>
                  <ul>
                    {dietPlan.general_notes.map((note, idx) => (
                      <li key={idx}>{note}</li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div className="diet-empty-state">
              <svg width="64" height="64" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
              </svg>
              <p>No diet plan available</p>
            </div>
          )}
        </div>

        {/* Footer */}
        {!loading && (
          <div className="diet-modal-footer">
            <button onClick={onClose} className="diet-footer-btn">
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Section Component
function DietSection({ title, icon, color, children }) {
  return (
    <div className="diet-section" style={{ borderColor: color }}>
      <div className="diet-section-header">
        <div className="diet-section-icon" style={{ background: color }}>
          {icon}
        </div>
        <h3>{title}</h3>
      </div>
      <div className="diet-section-content">
        {children}
      </div>
    </div>
  );
}

// Food Category Component
function FoodCategory({ title, foods, type }) {
  return (
    <div className={`food-category ${type}`}>
      <h4>{title}</h4>
      <ul>
        {foods.map((food, idx) => (
          <li key={idx}>{food}</li>
        ))}
      </ul>
    </div>
  );
}

export default DietModal;