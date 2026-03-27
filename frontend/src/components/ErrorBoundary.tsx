import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ errorInfo });
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  handleGoHome = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen bg-background flex items-center justify-center p-6" dir="rtl">
          <div className="max-w-md w-full text-center">
            <div className="w-20 h-20 rounded-3xl bg-amber-500/10 flex items-center justify-center mx-auto mb-6">
              <span className="text-4xl">⚠️</span>
            </div>
            <h2 className="text-xl font-bold text-foreground mb-2">
              حدث خطأ غير متوقع
            </h2>
            <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
              نعتذر عن هذا الخطأ. يرجى إعادة المحاولة أو العودة للصفحة الرئيسية.
            </p>
            {this.state.error && (
              <div className="mb-6 p-3 rounded-xl bg-muted/50 border border-border/10">
                <p className="text-xs text-muted-foreground font-mono break-all text-start" dir="ltr">
                  {this.state.error.message}
                </p>
              </div>
            )}
            <div className="flex gap-3 justify-center">
              <button
                onClick={this.handleRetry}
                className="px-6 py-3 rounded-2xl bg-emerald-600 text-white font-bold text-sm transition-all active:scale-95 hover:bg-emerald-700"
              >
                إعادة المحاولة
              </button>
              <button
                onClick={this.handleGoHome}
                className="px-6 py-3 rounded-2xl bg-muted text-foreground font-bold text-sm transition-all active:scale-95 hover:bg-muted/80"
              >
                الرئيسية
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
