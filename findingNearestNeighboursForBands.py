import pickle

def d(X,Y):
        d = 0
        na_val = -1.23e+34
        nm_val = 0
        d = (X - Y)**2
        return d

def getNNWavelength(wavelength, Ref):
#Ref is the list of tuples (wavelength, reflectance, s.d.) for a material
        d_min = None
        nearest = []
        na_val = -1.23e+34
        nm_val = 0
        for t in Ref:#t is a tuple
                if t[0] == na_val or t[0] == nm_val:
                        continue
                dist = d(wavelength,t[0])
                if dist != None or dist < d_min:
                        d_min = dist
                        del nearest[:]
                        nearest.append(t)
                if dist == d_min:       
                        nearest.append(t)
        return nearest

def distSig(sig, wavelengths):
        processed_wavelengths = {}
        processed_sig = {}
        na_val = -1.23e+34
        nm_val = 0
        for wavelength in wavelengths:
                processed_wavelengths[wavelength] = {}
                for c in sig:
                        processed_wavelengths[wavelength][c] = {}
                        for t in sig[c]:
                                processed_wavelengths[wavelength][c][t] = getNNWavelength(wavelength,sig[c][t])

        return processed_wavelengths

bandCentralWavelength = [522.2,547.4,572.6,597.8,622.9,648,673.1,698.2,723.2,748.3,773.3,798.3,823.2,848.2,873.1,898,922.9]
#scaled down
scaledWavelength = []
for wavelength in bandCentralWavelength:
        wavelength /= 1000
        scaledWavelength.append(wavelength)

print scaledWavelength

f = open('sig.p')
sig = pickle.load(f)
f.close()

nearestWavelengths = distSig(sig,scaledWavelength)
f = open('nearestWavelengths.p','w')
pickle.dump(nearestWavelengths,f)
f.close()
