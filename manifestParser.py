
class ManifestParser:
    #Parses the data so that I can actually use it
    def _split_line(self, line: str):
        first_comma = line.find('],')
        second_comma = line.find('}, ', first_comma + 1)

        if first_comma == -1 or second_comma == -1:
            raise ValueError("Line format incorrect")
        
        pos_part = line[:first_comma + 1]
        weight_part = line[first_comma + 2:second_comma + 1]
        desc_part = line[second_comma + 2:].strip()

        return pos_part, weight_part, desc_part
    
    def _parse_position(self,pos_str: str):
        inside = pos_str.strip()[1:-1]
        row_str, col_str = inside.split(',')
        return int(row_str), int(col_str)
    
    def _parse_weight(self, weight_str: str):
        inside = weight_str.strip()[1:-1]
        return int(inside)
    
    def parse_manifest(self, file_path: str):
        parsed = []

        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try: 
                    pos_part,weight_part,desc_part = self._split_line(line)
                    row, col = self._parse_position(pos_part)
                    weight = self._parse_weight(weight_part)
                    description = desc_part.strip()

                    parsed.append(((row,col),weight, description))

                except Exception as e:
                    print(f" Could not parse line:\n {line}\nReason: {e}")
                    continue

        return parsed
    
    
    
