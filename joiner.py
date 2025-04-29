import csv
import sys
import json

def main():
    minrowcount = float('inf')
    corpuses = []
    closeme = []
    header = None
    for category in sys.argv[1:]:
        csvf = open(f'fields{category}_norm.csv', 'r', newline='')
        reader = csv.DictReader(csvf, dialect='excel-tab')
        if header != None:
            protoheader = list(dict(next(reader)).keys())
            if protoheader != header:
                print('Warning: Different header present between files.')
        else:
            header = list(dict(next(reader)).keys())

        count = sum(1 for row in reader)
        if count < minrowcount:
            minrowcount = count

        corpuses.append(reader)
        csvf.seek(0)
        closeme.append(csvf)
    print(f'Min row count is {minrowcount}')

    with open(f'corpus_norm.csv', 'w', newline='') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=header, dialect='excel-tab')
        writer.writeheader()
        for cix, corpseg in enumerate(corpuses):
            next(corpseg) # Dispose of headers
            for i in range(minrowcount):
                print(i)
                nextrow = next(corpseg)
                nextrow.pop('')
                nextrow['section'] = sys.argv[cix + 1]
                json.dumps(print(nextrow))
                writer.writerow(nextrow)

if __name__ == "__main__":
    main()
