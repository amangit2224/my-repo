import React from 'react';
import '../App.css';

function DietModal({ isOpen, onClose, dietPlan, loading }) {
  if (!isOpen) return null;

  return (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px',
        overflowY: 'auto'
      }}
      onClick={onClose}
    >
      <div 
        style={{
          backgroundColor: 'white',
          borderRadius: '16px',
          maxWidth: '900px',
          width: '100%',
          maxHeight: '90vh',
          overflowY: 'auto',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
          position: 'relative'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{
          position: 'sticky',
          top: 0,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          padding: '24px 32px',
          borderRadius: '16px 16px 0 0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          zIndex: 10
        }}>
          <div>
            <h2 style={{ margin: 0, fontSize: '28px', fontWeight: '700' }}>
              🥗 Personalized Diet Plan
            </h2>
            <p style={{ margin: '8px 0 0', fontSize: '14px', opacity: 0.9 }}>
              Based on your medical report analysis
            </p>
          </div>
          <button 
            onClick={onClose}
            style={{
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              color: 'white',
              fontSize: '28px',
              cursor: 'pointer',
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background 0.2s'
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255, 255, 255, 0.3)'}
            onMouseLeave={(e) => e.target.style.background = 'rgba(255, 255, 255, 0.2)'}
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '32px' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '60px 20px' }}>
              <div className="spinner" style={{ margin: '0 auto 20px' }}></div>
              <p style={{ color: '#666', fontSize: '16px' }}>Generating your personalized diet plan...</p>
            </div>
          ) : dietPlan ? (
            <>
              {/* Conditions Detected */}
              {dietPlan.conditions_detected && dietPlan.conditions_detected.length > 0 && (
                <Section 
                  icon="🔍" 
                  title="Health Conditions Detected"
                  bgColor="#FEF3C7"
                  borderColor="#F59E0B"
                >
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {dietPlan.conditions_detected.map((condition, idx) => (
                      <span 
                        key={idx}
                        style={{
                          background: 'linear-gradient(135deg, #FBBF24, #F59E0B)',
                          color: 'white',
                          padding: '8px 16px',
                          borderRadius: '20px',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}
                      >
                        {condition.replace(/_/g, ' ').toUpperCase()}
                      </span>
                    ))}
                  </div>
                </Section>
              )}

              {/* Dietary Goals */}
              {dietPlan.dietary_goals && dietPlan.dietary_goals.length > 0 && (
                <Section 
                  icon="🎯" 
                  title="Your Dietary Goals"
                  bgColor="#DBEAFE"
                  borderColor="#3B82F6"
                >
                  <ul style={{ margin: 0, paddingLeft: '24px', lineHeight: '2' }}>
                    {dietPlan.dietary_goals.map((goal, idx) => (
                      <li key={idx} style={{ fontSize: '15px', color: '#1F2937' }}>
                        <strong>{goal}</strong>
                      </li>
                    ))}
                  </ul>
                </Section>
              )}

              {/* Foods to Eat */}
              {dietPlan.foods_to_eat && Object.keys(dietPlan.foods_to_eat).length > 0 && (
                <Section 
                  icon="✅" 
                  title="Foods to Include"
                  bgColor="#D1FAE5"
                  borderColor="#10B981"
                >
                  {Object.entries(dietPlan.foods_to_eat).map(([category, foods]) => (
                    foods && foods.length > 0 && (
                      <FoodCategory 
                        key={category} 
                        title={category.replace(/_/g, ' ').toUpperCase()} 
                        foods={foods}
                        color="#10B981"
                      />
                    )
                  ))}
                </Section>
              )}

              {/* Foods to Avoid */}
              {dietPlan.foods_to_avoid && Object.keys(dietPlan.foods_to_avoid).length > 0 && (
                <Section 
                  icon="⛔" 
                  title="Foods to Avoid/Limit"
                  bgColor="#FEE2E2"
                  borderColor="#EF4444"
                >
                  {Object.entries(dietPlan.foods_to_avoid).map(([riskLevel, foods]) => (
                    foods && foods.length > 0 && (
                      <FoodCategory 
                        key={riskLevel} 
                        title={riskLevel.replace(/_/g, ' ').toUpperCase()} 
                        foods={foods}
                        color="#EF4444"
                      />
                    )
                  ))}
                </Section>
              )}

              {/* Meal Suggestions */}
              {dietPlan.meal_suggestions && Object.keys(dietPlan.meal_suggestions).length > 0 && (
                <Section 
                  icon="🍽️" 
                  title="Sample Meal Ideas"
                  bgColor="#FCE7F3"
                  borderColor="#EC4899"
                >
                  {Object.entries(dietPlan.meal_suggestions).map(([mealTime, suggestions]) => (
                    suggestions && suggestions.length > 0 && (
                      <div key={mealTime} style={{ marginBottom: '20px' }}>
                        <h4 style={{ 
                          color: '#EC4899', 
                          fontSize: '16px', 
                          fontWeight: '600',
                          marginBottom: '10px',
                          textTransform: 'uppercase'
                        }}>
                          {mealTime.replace(/_/g, ' ')}
                        </h4>
                        <ul style={{ margin: 0, paddingLeft: '24px', lineHeight: '1.8' }}>
                          {suggestions.map((suggestion, idx) => (
                            <li key={idx} style={{ fontSize: '14px', color: '#374151' }}>
                              {suggestion}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )
                  ))}
                </Section>
              )}

              {/* Nutritional Targets */}
              {dietPlan.nutritional_targets && Object.keys(dietPlan.nutritional_targets).length > 0 && (
                <Section 
                  icon="📊" 
                  title="Nutritional Targets"
                  bgColor="#E0E7FF"
                  borderColor="#6366F1"
                >
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
                    gap: '16px' 
                  }}>
                    {Object.entries(dietPlan.nutritional_targets).map(([nutrient, target]) => (
                      <div 
                        key={nutrient}
                        style={{
                          background: 'white',
                          padding: '16px',
                          borderRadius: '8px',
                          border: '2px solid #6366F1'
                        }}
                      >
                        <div style={{ 
                          color: '#6366F1', 
                          fontSize: '14px', 
                          fontWeight: '600',
                          marginBottom: '6px',
                          textTransform: 'uppercase'
                        }}>
                          {nutrient.replace(/_/g, ' ')}
                        </div>
                        <div style={{ color: '#1F2937', fontSize: '14px' }}>
                          {target}
                        </div>
                      </div>
                    ))}
                  </div>
                </Section>
              )}

              {/* Lifestyle Tips */}
              {dietPlan.lifestyle_tips && dietPlan.lifestyle_tips.length > 0 && (
                <Section 
                  icon="💡" 
                  title="Lifestyle Tips"
                  bgColor="#FEF3C7"
                  borderColor="#F59E0B"
                >
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '12px' 
                  }}>
                    {dietPlan.lifestyle_tips.map((tip, idx) => (
                      <div 
                        key={idx}
                        style={{
                          background: 'white',
                          padding: '16px',
                          borderRadius: '8px',
                          border: '2px solid #F59E0B',
                          fontSize: '14px',
                          color: '#1F2937',
                          fontWeight: '500'
                        }}
                      >
                        {tip}
                      </div>
                    ))}
                  </div>
                </Section>
              )}

              {/* General Notes */}
              {dietPlan.general_notes && dietPlan.general_notes.length > 0 && (
                <div style={{
                  marginTop: '32px',
                  background: '#FEF9C3',
                  border: '2px solid #EAB308',
                  borderRadius: '12px',
                  padding: '20px'
                }}>
                  <h3 style={{ 
                    color: '#854D0E', 
                    fontSize: '18px', 
                    fontWeight: '700',
                    marginBottom: '12px'
                  }}>
                    📋 Important Notes
                  </h3>
                  <ul style={{ margin: 0, paddingLeft: '24px', lineHeight: '2' }}>
                    {dietPlan.general_notes.map((note, idx) => (
                      <li key={idx} style={{ fontSize: '14px', color: '#713F12' }}>
                        {note}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div style={{ textAlign: 'center', padding: '60px 20px' }}>
              <p style={{ color: '#666', fontSize: '16px' }}>No diet plan available</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{
          position: 'sticky',
          bottom: 0,
          background: '#F9FAFB',
          padding: '20px 32px',
          borderRadius: '0 0 16px 16px',
          borderTop: '1px solid #E5E7EB',
          display: 'flex',
          justifyContent: 'center'
        }}>
          <button 
            onClick={onClose}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              padding: '14px 40px',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'transform 0.2s, box-shadow 0.2s',
              boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)'
            }}
            onMouseEnter={(e) => {
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)';
            }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

// Section Component
function Section({ icon, title, bgColor, borderColor, children }) {
  return (
    <div style={{ 
      marginBottom: '28px',
      background: bgColor,
      border: `2px solid ${borderColor}`,
      borderRadius: '12px',
      padding: '24px'
    }}>
      <h3 style={{ 
        color: borderColor, 
        fontSize: '20px', 
        fontWeight: '700',
        marginBottom: '16px',
        display: 'flex',
        alignItems: 'center',
        gap: '10px'
      }}>
        <span style={{ fontSize: '24px' }}>{icon}</span>
        {title}
      </h3>
      {children}
    </div>
  );
}

// Food Category Component
function FoodCategory({ title, foods, color }) {
  return (
    <div style={{ marginBottom: '20px' }}>
      <h4 style={{ 
        color: color, 
        fontSize: '16px', 
        fontWeight: '600',
        marginBottom: '10px'
      }}>
        {title}
      </h4>
      <ul style={{ margin: 0, paddingLeft: '24px', lineHeight: '1.8' }}>
        {foods.map((food, idx) => (
          <li key={idx} style={{ fontSize: '14px', color: '#374151' }}>
            {food}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DietModal;