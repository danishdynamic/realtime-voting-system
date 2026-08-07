export interface Option {
  id: string;
  text: string;
  votes?: number;
}

export interface Poll {
  poll_id: string;
  question: string;
  options: Option[];
  start_time: string;
  end_time: string;
  status: 'upcoming' | 'active' | 'ended';
  time_remaining?: {
    hours: number;
    minutes: number;
    seconds: number;
    total_seconds: number;
  };
  badge_text?: string;
  results?: Record<string, number>;
  userVote?: string;
  total_votes?: number;
}

export interface VoteEvent {
  poll_id: string;
  results: Record<string, number>;
}

export interface CreatePollData {
  question: string;
  options: string[];
  created_by: string;
  start_time: string;
  end_time: string;
}