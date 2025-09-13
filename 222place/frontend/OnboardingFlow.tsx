/**
 * 222.place Onboarding Component
 * Bilingual onboarding flow for social matching
 */
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface Question {
  id: number;
  category: string;
  question_text: string;
  question_type: 'multiple_choice' | 'multi_select' | 'text' | 'scale';
  options?: string[];
  weight: number;
  is_required: boolean;
}

interface Response {
  question_id: number;
  response_value: string;
  metadata?: any;
}

interface Profile {
  display_name?: string;
  bio?: string;
  location_city?: string;
  location_lat?: number;
  location_lng?: number;
  preferred_language?: string;
}

const OnboardingFlow: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState<Response[]>([]);
  const [profile, setProfile] = useState<Profile>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchQuestions();
  }, [i18n.language]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const lang = i18n.language === 'es' ? 'es' : 'en';
      const response = await fetch(`/v1/social/onboarding/questions?lang=${lang}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch questions');
      }

      const data = await response.json();
      setQuestions(data.questions || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const handleResponse = (questionId: number, value: string) => {
    const existingIndex = responses.findIndex(r => r.question_id === questionId);
    const newResponse: Response = {
      question_id: questionId,
      response_value: value
    };

    if (existingIndex >= 0) {
      const newResponses = [...responses];
      newResponses[existingIndex] = newResponse;
      setResponses(newResponses);
    } else {
      setResponses([...responses, newResponse]);
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      setError(null);

      const submitData = {
        responses,
        profile: {
          ...profile,
          preferred_language: i18n.language
        }
      };

      const response = await fetch('/v1/social/onboarding/responses', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(submitData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to submit responses');
      }

      // Redirect to dashboard or next step
      window.location.href = '/dashboard';
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit responses');
    } finally {
      setSubmitting(false);
    }
  };

  const renderQuestion = (question: Question) => {
    const currentResponse = responses.find(r => r.question_id === question.id);

    switch (question.question_type) {
      case 'multiple_choice':
        return (
          <div className="space-y-3">
            {question.options?.map((option, index) => (
              <label key={index} className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="radio"
                  name={`question-${question.id}`}
                  value={option}
                  checked={currentResponse?.response_value === option}
                  onChange={(e) => handleResponse(question.id, e.target.value)}
                  className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        );

      case 'multi_select':
        const selectedValues = currentResponse?.response_value?.split(',') || [];
        return (
          <div className="space-y-3">
            {question.options?.map((option, index) => (
              <label key={index} className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  value={option}
                  checked={selectedValues.includes(option)}
                  onChange={(e) => {
                    const newValues = e.target.checked
                      ? [...selectedValues, option]
                      : selectedValues.filter(v => v !== option);
                    handleResponse(question.id, newValues.join(','));
                  }}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        );

      case 'text':
        return (
          <textarea
            value={currentResponse?.response_value || ''}
            onChange={(e) => handleResponse(question.id, e.target.value)}
            placeholder={t('onboarding.typeYourAnswer')}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
          />
        );

      case 'scale':
        return (
          <div className="space-y-4">
            <input
              type="range"
              min="1"
              max="5"
              value={currentResponse?.response_value || '3'}
              onChange={(e) => handleResponse(question.id, e.target.value)}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>1</span>
              <span>2</span>
              <span>3</span>
              <span>4</span>
              <span>5</span>
            </div>
          </div>
        );

      default:
        return <div className="text-red-500">Unsupported question type</div>;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-md">
          <h3 className="font-bold">{t('onboarding.error')}</h3>
          <p>{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            {t('onboarding.retry')}
          </button>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-800">{t('onboarding.noQuestions')}</h2>
          <p className="text-gray-600 mt-2">{t('onboarding.contactSupport')}</p>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const currentResponse = responses.find(r => r.question_id === currentQuestion.id);
  const canProceed = !currentQuestion.is_required || currentResponse?.response_value;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            {t('onboarding.title')}
          </h1>
          <p className="text-gray-600">
            {t('onboarding.subtitle')}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="max-w-2xl mx-auto mb-8">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>{t('onboarding.question')} {currentQuestionIndex + 1} {t('onboarding.of')} {questions.length}</span>
            <span>{Math.round(progress)}% {t('onboarding.complete')}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Question Card */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-6">
            {/* Category Badge */}
            <div className="mb-4">
              <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase tracking-wide">
                {currentQuestion.category}
              </span>
              {currentQuestion.is_required && (
                <span className="ml-2 text-red-500 text-sm">*</span>
              )}
            </div>

            {/* Question Text */}
            <h2 className="text-xl font-semibold text-gray-800 mb-6">
              {currentQuestion.question_text}
            </h2>

            {/* Question Input */}
            <div className="mb-8">
              {renderQuestion(currentQuestion)}
            </div>

            {/* Navigation Buttons */}
            <div className="flex justify-between">
              <button
                onClick={handlePrevious}
                disabled={currentQuestionIndex === 0}
                className={`px-6 py-2 rounded-lg font-medium ${
                  currentQuestionIndex === 0
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {t('onboarding.previous')}
              </button>

              {isLastQuestion ? (
                <button
                  onClick={handleSubmit}
                  disabled={!canProceed || submitting}
                  className={`px-6 py-2 rounded-lg font-medium ${
                    !canProceed || submitting
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-green-500 text-white hover:bg-green-600'
                  }`}
                >
                  {submitting ? t('onboarding.submitting') : t('onboarding.complete')}
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  disabled={!canProceed}
                  className={`px-6 py-2 rounded-lg font-medium ${
                    !canProceed
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-500 text-white hover:bg-blue-600'
                  }`}
                >
                  {t('onboarding.next')}
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Language Toggle */}
        <div className="text-center mt-8">
          <button
            onClick={() => i18n.changeLanguage(i18n.language === 'en' ? 'es' : 'en')}
            className="text-sm text-blue-600 hover:text-blue-800 underline"
          >
            {i18n.language === 'en' ? 'Cambiar a Español' : 'Switch to English'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingFlow;