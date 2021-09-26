import hashlib
import math

from sequence_base.models import Sequence


class SequenceService():
    def is_valid_sequence(self, letters):
        LIMIT = len(letters)
        valid_sequences = 0

        letters_hash = hashlib.md5(repr(letters).encode('utf-8')).hexdigest()
        sequence, created = Sequence.objects.get_or_create(
            letters_hash=letters_hash)
        sequence.letters = letters

        if not created:
            return sequence.is_valid

        columns = ["" for _ in range(LIMIT)]
        rows = ["" for _ in range(LIMIT)]
        diagonals = ["" for _ in range(2 * LIMIT - 1)]
        back_diagonals = ["" for _ in range(2 * LIMIT - 1)]
        min_back_diagonals = -LIMIT + 1

        for x in range(LIMIT):
            for y in range(LIMIT):
                columns[x] += letters[y][x]
                rows[y] += letters[y][x]
                diagonals[x+y] += letters[y][x]
                back_diagonals[x-y-min_back_diagonals] += letters[y][x]

        dimensions = [rows, columns, diagonals, back_diagonals]

        for dimension in dimensions:
            for row in dimension:
                if len(row) < 4:
                    continue

                current_letter = row[0]
                current_sequence_count = 1
                for letter in row[1:]:
                    if letter == current_letter:
                        current_sequence_count += 1
                    else:
                        if not current_sequence_count >= 4:
                            current_letter = letter
                            current_sequence_count = 1
                            continue

                        valid_sequences += math.ceil(
                            current_sequence_count / 4)
                        if valid_sequences >= 2:
                            sequence.is_valid = True
                            sequence.save()
                            return True

                    if current_sequence_count >= 4:
                        valid_sequences += math.ceil(
                            current_sequence_count / 4)
                        if valid_sequences >= 2:
                            sequence.is_valid = True
                            sequence.save()
                            return True

        sequence.is_valid = False
        sequence.save()
        return False

    def get_stats(self):
        sequences = Sequence.objects.all()
        valid = sequences.filter(is_valid=True).count()
        invalid = sequences.filter(is_valid=False).count()

        stats = {}
        stats["count_valid"] = valid
        stats["count_invalid"] = invalid
        stats["ratio"] = round(valid / (valid + invalid), 2)

        return stats
