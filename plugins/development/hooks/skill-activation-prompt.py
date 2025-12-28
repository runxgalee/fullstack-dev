import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, TypedDict


class PromptTriggers(TypedDict, total=False):
    keywords: List[str]
    intentPatterns: List[str]


class SkillRule(TypedDict):
    type: str  # 'guardrail' | 'domain'
    enforcement: str  # 'block' | 'suggest' | 'warn'
    priority: str  # 'critical' | 'high' | 'medium' | 'low'
    promptTriggers: Optional[PromptTriggers]


class SkillRules(TypedDict):
    version: str
    skills: Dict[str, SkillRule]


class HookInput(TypedDict):
    session_id: str
    transcript_path: str
    cwd: str
    permission_mode: str
    prompt: str


class MatchedSkill(TypedDict):
    name: str
    matchType: str  # 'keyword' | 'intent'
    config: SkillRule


def main():
    try:
        # Debug log
        import tempfile
        import datetime

        # Read input from stdin
        input_data = sys.stdin.read()

        print(tempfile.gettempdir())

        # Log input for debugging
        with open(tempfile.gettempdir() + '/skill-activation-debug.log', 'a') as log:
            log.write(f"\n[{datetime.datetime.now()}]\n")
            log.write(f"Input length: {len(input_data)} chars\n")
            if len(input_data) > 500:
                log.write(f"Input (truncated): {input_data[:500]}...\n")
            else:
                log.write(f"Input: {input_data}\n")

        data: HookInput = json.loads(input_data)
        prompt = data['prompt'].lower()

        # Log parsed prompt
        with open(tempfile.gettempdir() + '/skill-activation-debug.log', 'a') as log:
            log.write(f"Prompt: {prompt[:200]}\n")
            log.write(f"CLAUDE_PROJECT_DIR: {os.environ.get('CLAUDE_PROJECT_DIR', 'NOT SET')}\n")

        # Load skill rules
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR')
        if not project_dir:
            # Fallback to the actual project directory
            project_dir = os.path.expanduser('~/work/tf-observable-architecture-patterns')
        rules_path = Path(project_dir) / '.claude' / 'skills' / 'skill-rules.json'

        with open(rules_path, 'r', encoding='utf-8') as f:
            rules: SkillRules = json.load(f)

        matched_skills: List[MatchedSkill] = []

        # Check each skill for matches
        for skill_name, config in rules['skills'].items():
            triggers = config.get('promptTriggers')
            if not triggers:
                continue

            # Keyword matching
            if 'keywords' in triggers:
                keyword_match = any(
                    kw.lower() in prompt
                    for kw in triggers['keywords']
                )
                if keyword_match:
                    matched_skills.append({
                        'name': skill_name,
                        'matchType': 'keyword',
                        'config': config
                    })
                    continue

            # Intent pattern matching
            if 'intentPatterns' in triggers:
                intent_match = any(
                    re.search(pattern, prompt, re.IGNORECASE)
                    for pattern in triggers['intentPatterns']
                )
                if intent_match:
                    matched_skills.append({
                        'name': skill_name,
                        'matchType': 'intent',
                        'config': config
                    })

        # Log results
        with open(tempfile.gettempdir() + '/skill-activation-debug.log', 'a') as log:
            log.write(f"Matched skills: {[s['name'] for s in matched_skills]}\n")

        # Generate output if matches found
        if matched_skills:
            output = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            output += '🎯 SKILL ACTIVATION CHECK\n'
            output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'

            # Group by priority
            critical = [s for s in matched_skills if s['config']['priority'] == 'critical']
            high = [s for s in matched_skills if s['config']['priority'] == 'high']
            medium = [s for s in matched_skills if s['config']['priority'] == 'medium']
            low = [s for s in matched_skills if s['config']['priority'] == 'low']

            if critical:
                output += '⚠️ CRITICAL SKILLS (REQUIRED):\n'
                for s in critical:
                    output += f"  → {s['name']}\n"
                output += '\n'

            if high:
                output += '📚 RECOMMENDED SKILLS:\n'
                for s in high:
                    output += f"  → {s['name']}\n"
                output += '\n'

            if medium:
                output += '💡 SUGGESTED SKILLS:\n'
                for s in medium:
                    output += f"  → {s['name']}\n"
                output += '\n'

            if low:
                output += '📌 OPTIONAL SKILLS:\n'
                for s in low:
                    output += f"  → {s['name']}\n"
                output += '\n'

            output += 'ACTION: Use Skill tool BEFORE responding\n'
            output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'

            print(output, end='')

        sys.exit(0)
    except Exception as err:
        import traceback
        import tempfile
        import datetime

        error_msg = f'Error in skill-activation-prompt hook: {err}\n{traceback.format_exc()}'

        # Log error for debugging
        try:
            with open(tempfile.gettempdir() + '/skill-activation-debug.log', 'a') as log:
                log.write(f"\n[{datetime.datetime.now()}] ERROR\n")
                log.write(error_msg + '\n')
        except:
            pass

        print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
