import time
import random

word_list = [
        'python', 'developer', 'keyboard', 'artificial', 'algorithm', 'data', 'syntax', 'variable', 'function',
            'loop', 'object', 'input', 'output', 'error', 'model', 'debug', 'framework', 'library', 'script', 'software',
            'interface', 'database', 'network', 'server', 'client', 'cloud', 'machine', 'learning', 'testing', 'deployment', 'version',
            'control', 'repository', 'commit', 'branch', 'merge', 'pull', 'push', 'issue', 'bug', 'feature', 'release', 'usability', 'security',
            'privacy', 'encryption', 'protocol', 'api', 'endpoint', 'request', 'response', 'header', 'body', 'status', 'code', 'json',
            'xml', 'html', 'css', 'javascript', 'frontend', 'backend', 'fullstack', 'devops', 'agile', 'scrum', 'java', 'sprint', 'standup',
            'planning', 'task', 'story', 'epic', 'workflow', 'pipeline', 'continuous', 'delivery', 'deployment', 'monitoring', 'logging',
            'analytics', 'dashboard', 'reporting', 'insights', 'feedback', 'iteration', 'teamwork', 'project', 'management', 'tools', 'setup',
            'package', 'versioning', 'testing', 'unit', 'system', 'acceptance', 'regression', 'load', 'stress', 'usability', 'user', 'experience',
            'interface', 'design', 'prototype', 'mockup', 'wireframe', 'style', 'guide', 'branding', 'identity', 'content', 'strategy',
            'marketing', 'seo', 'social', 'media', 'analytics', 'conversion', 'campaign', 'branding', 'audience', 'engagement', 'reach', 'impression',
            'click', 'rate', 'lead', 'funnel', 'sales', 'pipeline', 'customer', 'management', 'support', 'service', 'feedback', 'survey',
            'insight', 'analysis', 'research', 'risk', 'compliance', 'regulation', 'policy', 'procedure', 'governance', 'audit', 'report', 'knowledge', 'base',
            'logic', 'condition', 'iterate', 'recursion', 'exception', 'performance', 'optimizate', 'scalable', 'github', 'stable', 'jawa'
    ]

def typing_trainer(words, num_words=25):
    random.shuffle(words)
    words = words[:num_words]

    typed_words = []
    start_time = time.time()
    input("\npress enter to start...")
    for i in range(num_words):
        line_display = []
        for j, word in enumerate(words[i:]):
            if j == 0:
                line_display.append(f">>> {word} <<<")
            else:
                line_display.append(word)
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print("\nremaining:", " ".join(line_display))

        typed = input("input: ").strip()
        typed_words.append(typed)

    end_time = time.time()
    elapsed = end_time - start_time

    correct = sum(1 for a, b in zip(words, typed_words) if a == b)
    accuracy = round((correct / num_words) * 100, 2)
    wpm = round(num_words / (elapsed / 60))

    print("\n--- final stats ---")
    print(f"time taken: {round(elapsed, 2)} seconds")
    print(f"words per minute (wpm): {wpm}")
    print(f"accuracy: {accuracy}%")

if __name__ == "__main__":
    typing_trainer(words=word_list)